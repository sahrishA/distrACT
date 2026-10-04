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

from activity import (
    create_activity,
    get_or_create_student,
    get_student_activities,
)
from auth import auth, login_manager
from config import Config
from modelui import db
from models import create_tables

from google_calendar import (
    create_oauth_flow,
    credentials_from_dict,
    fetch_calendar_events,
    google_account_email,
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

    activities = get_student_activities(current_student_id())

    return render_template(
        "dashboard.html",
        calendar_connected=calendar_connected,
        calendar_events=calendar_events,
        activities=activities,
    )


def current_student_id():
    """Activities are keyed by the Students table, linked to users by email."""
    return get_or_create_student(current_user.username, current_user.email)


@app.route("/activities/add", methods=["GET", "POST"])
@login_required
def add_activity():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        date = request.form.get("date", "")
        start_time = request.form.get("start_time", "")
        end_time = request.form.get("end_time", "")

        if not title or not date or not start_time or not end_time:
            flash("Please fill in the title, date, start time and end time.", "error")
        elif end_time <= start_time:
            flash("End time must be after start time.", "error")
        else:
            create_activity(
                current_student_id(),
                title,
                date,
                start_time,
                end_time,
                description or None,
            )
            flash("Activity added!", "success")
            return redirect(url_for("dashboard"))

    return render_template("add_activity.html", form=request.form)


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


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
        # Always show the account chooser, pre-filled with this user's email,
        # so a Google account already signed in to the browser isn't reused.
        prompt="select_account consent",
        login_hint=current_user.email,
    )

    if returned_state != state:
        return "OAuth state mismatch", 400

    # Newer google-auth-oauthlib versions use PKCE; the callback builds a new
    # flow, so it needs the same code verifier to exchange the code.
    session["google_code_verifier"] = getattr(flow, "code_verifier", None)

    return redirect(authorization_url)


# Google Calendar: OAuth callback
@app.route("/oauth2callback")
@login_required
def oauth2callback():
    """Handle Google's redirect after authorization."""

    code_verifier = session.pop("google_code_verifier", None)

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
        if code_verifier:
            flow.code_verifier = code_verifier
        flow.fetch_token(authorization_response=request.url)

        # Only accept the Google account that matches the logged-in user.
        google_email = google_account_email(flow.credentials)
        if google_email != current_user.email.strip().lower():
            flash(
                f"Please connect the Google account for {current_user.email}. "
                f"You signed in to Google as {google_email or 'an unknown account'}.",
                "error",
            )
            return redirect(url_for("dashboard"))

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


