
import os
from datetime import datetime, timedelta, timezone

from flask import current_app
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


def create_oauth_flow(state=None):
    """Create the OAuth flow used to connect Google Calendar."""
    client_file = current_app.config["GOOGLE_CLIENT_SECRETS_FILE"]

    if not os.path.isabs(client_file):
        client_file = os.path.join(
            current_app.root_path,
            client_file,
        )

    flow = Flow.from_client_secrets_file(
        client_file,
        scopes=current_app.config["GOOGLE_SCOPES"],
        state=state,
    )

    flow.redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
    return flow


def build_calendar_service(credentials):
    """Create an authenticated Google Calendar API client."""
    return build(
        "calendar",
        "v3",
        credentials=credentials,
        cache_discovery=False,
    )


def fetch_calendar_events(credentials, days_ahead=14):
    """Fetch upcoming events and return normalized event dictionaries."""
    service = build_calendar_service(credentials)

    now = datetime.now(timezone.utc)
    end = now + timedelta(days=days_ahead)

    events = []
    page_token = None

    while True:
        response = service.events().list(
            calendarId="primary",
            timeMin=now.isoformat(),
            timeMax=end.isoformat(),
            maxResults=250,
            singleEvents=True,
            orderBy="startTime",
            pageToken=page_token,
        ).execute()

        for item in response.get("items", []):
            if item.get("status") == "cancelled":
                continue

            start_data = item.get("start", {})
            end_data = item.get("end", {})

            start_value = (
                start_data.get("dateTime")
                or start_data.get("date")
            )
            end_value = (
                end_data.get("dateTime")
                or end_data.get("date")
            )

            if not start_value or not end_value:
                continue

            events.append({
                "id": f"google:{item['id']}",
                "source": "google_calendar",
                "title": item.get("summary") or "Busy",
                "start": start_value,
                "end": end_value,
                "all_day": (
                    "date" in start_data
                    and "dateTime" not in start_data
                ),
            })

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return events


def credentials_from_dict(data):
    """Reconstruct OAuth credentials from a stored dictionary."""
    return Credentials.from_authorized_user_info(data)