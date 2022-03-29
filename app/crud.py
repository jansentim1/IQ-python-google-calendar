import datetime

from app.db import db
from app.logging import log

log = log.getChild("crud")


def update_meeting_time(start_event, meeting):
    tz1 = datetime.datetime.fromisoformat(meeting["first_expert"]["status"][0]["date"]).tzinfo
    tz2 = datetime.datetime.fromisoformat(meeting["second_expert"]["status"][0]["date"]).tzinfo
    db.meets.update_one(
        {"meeting_id": meeting["meeting_id"]},
        {
            "$set": {
                "proposed_time": start_event.isoformat(),
                "first_expert.status.0.date": start_event.astimezone(tz1).isoformat(),
                "second_expert.status.0.date": start_event.astimezone(tz2).isoformat(),
            }
        },
    )


def decline_meeting(meeting, expert):
    db.meets.update_one(
        {"meeting_id": meeting["meeting_id"]},
        {"$set": {"admin_status": "cancelled"}},
        {
            "$push": {
                expert
                + ".status": {
                    "status": "declined",
                    "reason": {"selected": "Other", "explanation": "automated from google calendar"},
                    "timestamp": datetime.datetime.now().isoformat(),
                }
            }
        },
    )

    log.info(f"removed {meeting['meeting_id']}")


def update_meeting_status(meeting, s1, s2):
    db.meets.update_one(
        {"meeting_id": meeting["meeting_id"]},
        {"$set": {"first_expert.status.0.status": s1, "second_expert.status.0.status": s2}},
    )
