"""

InQommon google calendar automation

"""
import time
from app.synching import start_google_cronjob

# from app.utils import send_slack_message


if __name__ == "__main__":
    while True:
        # try:
        start_google_cronjob()
        # except Exception:
        #     print("Update failed, wait for 1 minute and continue")
        # send_slack_message('test', 'test')
        break
        for i in range(1):
            print(f"{1-i} minutes left before next script runs")
            time.sleep(60)
