import json
import requests


def send_slack_message(webhook, payload):

    return requests.post(webhook, json.dumps(payload))
