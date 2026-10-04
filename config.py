
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///distract.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_CLIENT_SECRETS_FILE = os.getenv(
        "GOOGLE_CLIENT_SECRETS_FILE",
        "credentials.json",
    )

    GOOGLE_REDIRECT_URI = os.getenv(
        "GOOGLE_REDIRECT_URI",
        "http://127.0.0.1:5000/oauth2callback",
    )

    # Allow OAuth over plain http for local development only.
    if GOOGLE_REDIRECT_URI.startswith(("http://127.0.0.1", "http://localhost")):
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

    # Google may return previously granted scopes too; don't treat that as an error.
    os.environ.setdefault("OAUTHLIB_RELAX_TOKEN_SCOPE", "1")

    # Read-only access to the user's calendar events.
    GOOGLE_SCOPES = [
        "https://www.googleapis.com/auth/calendar.events.readonly"
    ]