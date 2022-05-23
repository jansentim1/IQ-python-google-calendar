import datetime
import pytz
from googleapiclient.discovery import build
from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client

from app.logging import log

CLIENT_ID = "292411058500-29a2ptcf11bfkrb9mg3kk6b12dmk3jmo.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = (
    "1//09PMIB0Izz8unCgYIARAAGAkSNwF-L9IrhZu_XCFEiN47Jyh0C4dsz8KndHtLVluwkjHZuSs3KV9CZ1rxniJWG6azrlKSInfzouQ"
)


def get_calendar_service():
    creds_new = client.OAuth2Credentials(
        access_token=None,  # set access_token to None since we use a refresh token
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=REFRESH_TOKEN,
        token_expiry=None,
        token_uri=GOOGLE_TOKEN_URI,
        user_agent=None,
        revoke_uri=GOOGLE_REVOKE_URI,
    )

    service = build("calendar", "v3", credentials=creds_new)
    log.info(f"calendar service has started {service}")
    return service


def get_google_event(event_id, google_calendar_service):
    event = google_calendar_service.events().get(calendarId="primary", eventId=event_id).execute()
    if not event:
        log.critical("Event not found")
        return None
    return event


def delete_calendar_event(event_id, google_calendar_service):
    if not event_id:
        return
    event = google_calendar_service.events().get(calendarId="primary", eventId=event_id).execute()
    log.info(event_id + " has been removed")
    if event:
        google_calendar_service.events().delete(calendarId="primary", eventId=event_id, sendUpdates="none").execute()


def update_google_event(event_id, event, meeting, proposed_time, google_calendar_service):
    d = proposed_time.astimezone(pytz.utc).replace(tzinfo=None)
    start = d.isoformat() + "Z"
    end = (d + datetime.timedelta(minutes=45)).isoformat() + "Z"

    event["start"] = {"dateTime": start, "timeZone": "Europe/Amsterdam"}
    event["end"] = {"dateTime": end, "timeZone": "Europe/Amsterdam"}
    if meeting["first_expert"]["status"][0]["status"] == "accepted":
        r1 = "accepted"
    else:
        r1 = "needsAction"

    if meeting["second_expert"]["status"][0]["status"] == "accepted":
        r2 = "accepted"
    else:
        r2 = "needsAction"

    google_calendar_service.events().update(
        calendarId="primary", eventId=event_id, body=event, sendUpdates="all"
    ).execute()

    event = get_google_event(event_id, google_calendar_service)
    event["attendees"][0]["email"] = meeting["first_expert"]["email"]
    event["attendees"][0]["displayName"] = meeting["first_expert"]["name"]
    event["attendees"][0]["responseStatus"] = r1
    event["attendees"][1]["email"] = meeting["second_expert"]["email"]
    event["attendees"][1]["displayName"] = meeting["second_expert"]["name"]
    event["attendees"][1]["responseStatus"] = r2
    google_calendar_service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
