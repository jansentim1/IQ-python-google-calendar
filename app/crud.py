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
