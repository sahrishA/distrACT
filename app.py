import json
import secrets

from flask import (
    Flask,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
)

from flask_login import current_user, login_required

from auth import auth, login_manager
from config import Config
from modelui import db
from models import create_tables

from google_calendar import (
    create_oauth_flow,
    credentials_from_dict,
    fetch_calendar_events,
)


# Initialize Flask app ONCE, before defining routes
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager.init_app(app)
app.register_blueprint(auth)


# Initialize database tables
with app.app_context():
    db.create_all()
    create_tables()


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))


@app.route("/dashboard")
@login_required
def dashboard():
    calendar_connected = bool(current_user.google_credentials)
    calendar_events = []

    if calendar_connected:
        try:
            credentials = credentials_from_dict(
                json.loads(current_user.google_credentials)
            )
            calendar_events = fetch_calendar_events(credentials)

            # Save the access token if Google refreshed it
            if credentials.to_json() != current_user.google_credentials:
                current_user.google_credentials = credentials.to_json()
                db.session.commit()

        except Exception:
            current_app.logger.exception("Could not load Google Calendar events")
            db.session.rollback()
            flash(
                "Could not load your Google Calendar. Try reconnecting.",
                "warning",
            )

    return render_template(
        "dashboard.html",
        calendar_connected=calendar_connected,
        calendar_events=calendar_events,
    )


# Google Calendar: Connect
@app.route("/calendar/connect")
@login_required
def calendar_connect():
    """Start Google Calendar authorization."""

    state = secrets.token_urlsafe(32)
    session["google_oauth_state"] = state

    flow = create_oauth_flow(state=state)

    authorization_url, returned_state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    if returned_state != state:
        return "OAuth state mismatch", 400

    return redirect(authorization_url)


# Google Calendar: OAuth callback
@app.route("/oauth2callback")
@login_required
def oauth2callback():
    """Handle Google's redirect after authorization."""

    if request.args.get("error"):
        session.pop("google_oauth_state", None)
        flash(
            "Google Calendar connection was cancelled or denied.",
            "warning",
        )
        return redirect(url_for("dashboard"))

    expected_state = session.pop("google_oauth_state", None)
    received_state = request.args.get("state")

    if (
        not expected_state
        or not received_state
        or not secrets.compare_digest(
            expected_state,
            received_state,
        )
    ):
        return "Invalid OAuth state. Please try connecting again.", 400

    try:
        flow = create_oauth_flow(state=expected_state)
        flow.fetch_token(authorization_response=request.url)

        current_user.google_credentials = flow.credentials.to_json()
        db.session.commit()

    except Exception:
        current_app.logger.exception("Google Calendar OAuth failed")
        db.session.rollback()
        flash(
            "Could not connect Google Calendar. Please try again.",
            "error",
        )
        return redirect(url_for("dashboard"))

    flash("Google Calendar connected successfully!", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)


