"""

InQommon google calendar automation

"""
import time
from app.logging import log
from app.synching import start_google_cronjob, start_placeholder_cronjob

# from app.utils import send_slack_message


if __name__ == "__main__":
    while True:
        try:
            start_google_cronjob()
        except Exception as e:
            log.critical("Update failed, wait for 1 minute and continue: " + str(e))
            webhook = "https://hooks.slack.com/services/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"
            payload = {"text": "Google Calendar API not working! CHECK NOW"}
            # send_slack_message(webhook, payload)
        try:
            start_placeholder_cronjob()
        except Exception as e:
            log.critical("Update failed, wait for 1 minute and continue: " + str(e))
            webhook = "https://hooks.slack.com/services/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"
            payload = {"text": "placeholder cronjob not working! CHECK NOW"}
            # send_slack_message(webhook, payload)
        for i in range(5):
            log.info(f"{5-i} minutes left before next script runs")
            time.sleep(60)
