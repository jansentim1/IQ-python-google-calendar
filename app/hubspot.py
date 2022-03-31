import datetime
import json
import requests

from app.config import config


def send_share_contact_details(meeting):
    headers = {}
    headers["Content-Type"] = "application/json"

    url1 = (
        "https://api.hubapi.com/contacts/v1/contact/email/"
        + meeting["first_expert"]["email"]
        + "/profile?hapikey="
        + config.HAPIKEY
    )
    url2 = (
        "https://api.hubapi.com/contacts/v1/contact/email/"
        + meeting["second_expert"]["email"]
        + "/profile?hapikey="
        + config.HAPIKEY
    )

    data1 = json.dumps(
        {
            "properties": [
                {"property": "wsm_first_name_expert_1", "value": meeting["first_expert"]["first_name"]},
                {
                    "property": "wsm___confirmed_meeting_date_and_time",
                    "value": datetime.datetime.fromisoformat(meeting["first_expert"]["status"][0]["date"]).strftime(
                        "%m/%d/%Y, %H:%M:%S, %Z"
                    ),
                },
                {"property": "wsm___full_name_expert_2", "value": meeting["second_expert"]["name"]},
                {"property": "wsm___email_address_expert_2", "value": meeting["second_expert"]["email"]},
                {"property": "wsm___first_name_expert_2", "value": meeting["second_expert"]["first_name"]},
                {"property": "wsm___trigger___confirmation_meeting_sharing_contact_details", "value": True},
            ]
        }
    )
    data2 = json.dumps(
        {
            "properties": [
                {"property": "wsm_first_name_expert_1", "value": meeting["second_expert"]["first_name"]},
                {
                    "property": "wsm___confirmed_meeting_date_and_time",
                    "value": datetime.datetime.fromisoformat(meeting["second_expert"]["status"][0]["date"]).strftime(
                        "%m/%d/%Y, %H:%M:%S, %Z"
                    ),
                },
                {"property": "wsm___full_name_expert_2", "value": meeting["first_expert"]["name"]},
                {"property": "wsm___email_address_expert_2", "value": meeting["first_expert"]["email"]},
                {"property": "wsm___first_name_expert_2", "value": meeting["first_expert"]["first_name"]},
                {"property": "wsm___trigger___confirmation_meeting_sharing_contact_details", "value": True},
            ]
        }
    )

    r1 = requests.post(data=data1, url=url1, headers=headers)
    r2 = requests.post(data=data2, url=url2, headers=headers)
    return (r1.content, r2.content)


def send_accept_meeting(meeting, expert1, expert2):
    headers = {}
    headers["Content-Type"] = "application/json"
    url = (
        "https://api.hubapi.com/contacts/v1/contact/email/"
        + meeting[expert2]["email"]
        + "/profile?hapikey="
        + config.HAPIKEY
    )
    data = json.dumps(
        {
            "properties": [
                {"property": "wsm___trigger___status_meeting___accepted", "value": True},
                {"property": "wsm_first_name_expert_1", "value": meeting[expert2]["first_name"]},
                {"property": "wsm___full_name_expert_2", "value": meeting[expert1]["first_name"]},
                {
                    "property": "wsm___first_proposed_meeting_invitation",
                    "value": datetime.datetime.fromisoformat(meeting[expert2]["status"][0]["date"]).strftime(
                        "%m/%d/%Y, %H:%M:%S, %Z"
                    ),
                },
            ]
        }
    )

    r1 = requests.post(data=data, url=url, headers=headers)
    return r1.content


def send_declined_meeting(meeting, expert1, expert2):
    headers = {}
    headers["Content-Type"] = "application/json"
    url = (
        "https://api.hubapi.com/contacts/v1/contact/email/"
        + meeting[expert2]["email"]
        + "/profile?hapikey="
        + config.HAPIKEY
    )
    data = json.dumps(
        {
            "properties": [
                {"property": "wsm___trigger___status_meeting___declined", "value": True},
                {"property": "wsm_first_name_expert_1", "value": meeting[expert2]["first_name"]},
                {"property": "wsm___full_name_expert_2", "value": meeting[expert1]["first_name"]},
            ]
        }
    )

    r1 = requests.post(data=data, url=url, headers=headers)
    return r1.status_code
