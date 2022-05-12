import time
import datetime
import requests
import json

from app.config import config
from app.crud import update_meeting_status, update_meeting_time, decline_meeting
from app.db import db
from app.logging import log
from app.google_calendar import get_google_event, get_calendar_service, delete_calendar_event  # , update_google_event
from app.hubspot import send_share_contact_details, send_accept_meeting, send_declined_meeting


def start_google_cronjob():

    start_time = time.time()
    log.info("%s is the start-time" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
    log.info("the job is running")
    google_calendar_service = get_calendar_service()
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    cursor = db.meets.find({"proposed_time": {"$gte": date.isoformat()}})
    for meeting in cursor:

        if not meeting.get("google_event_id"):
            continue

        event_id = meeting["google_event_id"]
        log.info(event_id)
        # if not event_id == "asfi70b0u":
        #     continue
        event = get_google_event(event_id, google_calendar_service)
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
            # update_google_event(event_id,event, meeting, proposed_time, google_calendar_service)
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

        if r1 == "accepted" and s1 == "pending":
            s1 = "accepted"
            changed_status_1 = True
        elif r1 == "declined" and meeting["admin_status"] != "cancelled":
            decline_meeting(meeting, "first_expert")
            send_declined_meeting(meeting, "first_expert", "second_expert")
            delete_calendar_event(event_id, google_calendar_service)
        if r2 == "accepted" and s2 == "pending":
            s2 = "accepted"
            changed_status_2 = True
        elif r2 == "declined" and meeting["admin_status"] != "cancelled":
            decline_meeting(meeting, "second_expert")
            send_declined_meeting(meeting, "second_expert", "first_expert")
            delete_calendar_event(event_id, google_calendar_service)

        if changed_status_1 or changed_status_2:
            if s1 == "accepted" and s2 == "accepted":
                log.info(send_share_contact_details(meeting))
            elif s1 == "accepted":
                log.info(send_accept_meeting(meeting, "first_expert", "second_expert"))
            else:
                log.info(send_accept_meeting(meeting, "second_expert", "first_expert"))
            update_meeting_status(meeting, s1, s2)


def start_placeholder_cronjob():
    l = []
    for i in db.meetonboardings.find():
        if not i["step_timestamps"]["introduction"]:
            continue

        flexible = i["availability"]["flexibleSlots"]
        unsubscribed = i["availability"]["break"].get("unsubscribed")
        if unsubscribed:
            continue
        if i.get("matching_poule", "lkjh") == "testing":
            continue

        if flexible:
            for meeting_request in flexible:
                if not meeting_request.get("placeholder_google_ids") and meeting_request["requestCompleted"] == False:

                    net = db.networkers.find_one({"uuid": i["uuid"]})
                    if "+" in net["email"]:
                        print("fake account", net["email"])
                        continue
                    l.append(
                        (
                            net["email"],
                            i["uuid"],
                            meeting_request["hub"],
                            meeting_request["times"],
                            meeting_request["requestCompleted"],
                            meeting_request["timestamp"],
                            meeting_request["request_id"],
                        )
                    )
    log.info(len(l))

    if l:
        endpoint = "https://inqommon.com/matcher_api/login"
        files = {"username": (None, config.USERNAME_MATCHER), "password": (None, config.PASSWORD_MATCHER)}
        response_auth = requests.post(endpoint, files=files)
        bearer = response_auth.json()["access_token"]

        h = {"accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer " + bearer}

        for i in l:
            log.info(f"{i[1]} starting")
            d = json.dumps(i[3])
            endpoint = (
                "https://inqommon.com/matcher_api/matching_job/set_placeholders?uuid="
                + i[1]
                + "&hub="
                + i[2]
                + "&requestcompleted="
                + str(i[4])
                + "&timestamp="
                + i[5]
                + "&request_id="
                + i[6]
            )
            response = requests.post(endpoint, headers=h, data=d).json()
            log.info(f"{i[0]},{response}")
            time.sleep(30)
