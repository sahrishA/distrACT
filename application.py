from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from modelui import db
from auth import auth, login_manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-change-later"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///distract.db"

db.init_app(app)
login_manager.init_app(app)
app.register_blueprint(auth)

@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)