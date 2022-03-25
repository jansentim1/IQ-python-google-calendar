import time
import datetime

# from app.crud import update_meeting_time
from app.db import db
from app.logging import log
from app.google_calendar import get_google_event  # , update_google_event


def start_google_cronjob():

    start_time = time.time()
    log.info("%s is the start-time" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))
    log.info("the job is running")

    cursor = db.meets.find({"proposed_time": {"$gte": datetime.datetime.now().isoformat()}})
    for meeting in cursor:

        if not meeting.get("google_event_id"):
            continue

        event_id = meeting["google_event_id"]
        # if not event_id == 'asfi70b0u':
        #     continue
        event = get_google_event(event_id)
        start_event = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        proposed_time = datetime.datetime.fromisoformat(meeting["proposed_time"])
        if start_event != proposed_time:
            print("NOT SAME DATE")
            print(event_id)
            print(start_event, proposed_time)
            print(meeting["first_expert"]["name"])
            print(meeting["second_expert"]["name"])

            # update_meeting_time(start_event, meeting)
            # print(update_google_event(event_id,event, meeting, proposed_time))

        else:
            print("SAME")

        # else:
        # print('SAME DATE')
        # print(event_id)
        # print(start_event, proposed_time)
        # log.info(meeting['first_expert']['status'][0]['status'])
        # log.info(meeting['second_expert']['status'][0]['status'])
