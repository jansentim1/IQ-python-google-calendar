import time
import datetime

from app.crud import update_meeting_status, update_meeting_time, decline_meeting
from app.db import db
from app.logging import log
from app.google_calendar import get_google_event  # , update_google_event
from app.hubspot import send_share_contact_details, send_accept_meeting


def start_google_cronjob():

    start_time = time.time()
    log.info("%s is the start-time" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
    log.info("the job is running")

    cursor = db.meets.find({"proposed_time": {"$gte": datetime.datetime.now().isoformat()}})
    for meeting in cursor:

        if not meeting.get("google_event_id"):
            continue

        event_id = meeting["google_event_id"]
        if not event_id == "asfi70b0u":
            continue
        event = get_google_event(event_id)
        start_event = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        proposed_time = datetime.datetime.fromisoformat(meeting["proposed_time"])
        if start_event != proposed_time:
            log.info("NOT SAME DATE")
            log.info(event_id)
            log.info(start_event)
            log.info(proposed_time)
            log.info(meeting["first_expert"]["name"])
            log.info(meeting["second_expert"]["name"])
            update_meeting_time(start_event, meeting)
            # update_google_event(event_id,event, meeting, proposed_time)
        else:
            pass

        changed_status_1 = False
        changed_status_2 = False
        if event["attendees"][0]["email"] == meeting["first_expert"]["email"]:
            r1 = event["attendees"][0]["responseStatus"]
            r2 = event["attendees"][1]["responseStatus"]

        elif event["attendees"][0]["email"] == meeting["second_expert"]["email"]:
            r2 = event["attendees"][0]["responseStatus"]
            r1 = event["attendees"][1]["responseStatus"]

        s1 = meeting["first_expert"]["status"][0]["status"]
        s2 = meeting["second_expert"]["status"][0]["status"]
        log.info(s1)
        log.info(s2)
        if r1 == "accepted" and s1 == "pending":
            s1 = "accepted"
            changed_status_1 = True
        elif r1 == "declined" and meeting["admin_status"] != "cancelled":
            decline_meeting(meeting, "first_expert", "second_expert")
        if r2 == "accepted" and s2 == "pending":
            s2 = "accepted"
            changed_status_2 = True
        elif r2 == "declined" and meeting["admin_status"] != "cancelled":
            decline_meeting(meeting, "second_expert", "first_expert")

        if changed_status_1 or changed_status_2:
            if s1 == "accepted" and s2 == "accepted":
                log.info(send_share_contact_details(meeting))
            elif s1 == "accepted":
                log.info(send_accept_meeting(meeting, "first_expert", "second_expert"))
            else:
                log.info(send_accept_meeting(meeting, "second_expert", "first_expert"))
            update_meeting_status(meeting, s1, s2)
