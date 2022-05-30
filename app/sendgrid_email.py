import datetime
import re
import pytz

from app.config import config

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(email, html_content, subject):
    """Send Emails

    Send email to the mail ids
    :param emails: emails of the user
    :type emails: list
    :param notification_text: notification text
    :type notification_text: str
    :param request_link: link to the requet
    :type request_link: str
    :param subject: subject of the email
    :type subject: str

    :rtype: str
    """
    message = Mail(from_email="hello@inqommon.com", to_emails=[email], subject=subject, html_content=html_content)
    try:
        sg = SendGridAPIClient(config.SENDGRID_KEY)
        sg.send(message)
        return f"Email Sent to {email}"
    except Exception as e:
        return "email not sent to: " + email + str(e.message)


def send_share_contact_details(meeting):

    # Read in the file
    with open(config.ROOT_DIR / "html_templates/sharing_details_status_meeting.html", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("CONTACT.WSM_FIRST_NAME_EXPERT_1", meeting["first_expert"]["first_name"])
    filedata = filedata.replace(
        "CONTACT.WSM___CONFIRMED_MEETING_DATE_AND_TIME",
        datetime.datetime.fromisoformat(meeting["first_expert"]["status"][0]["date"]).strftime(
            "%m/%d/%Y, %H:%M:%S, %Z"
        ),
    )
    filedata = filedata.replace("CONTACT.WSM___FULL_NAME_EXPERT_2", meeting["second_expert"]["name"])
    filedata = filedata.replace("CONTACT.WSM___EMAIL_ADDRESS_EXPERT_2", meeting["second_expert"]["email"])
    filedata = filedata.replace("CONTACT.WSM___FIRST_NAME_EXPERT_2", meeting["second_expert"]["first_name"])

    title = re.findall('"([^"]*)"', filedata.split('<meta property="og:title" content=')[1])[0]
    email = meeting["first_expert"]["email"]
    s1 = send_email(email, filedata, title)

    # Read in the file
    with open(config.ROOT_DIR / "html_templates/sharing_details_status_meeting.html", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("CONTACT.WSM_FIRST_NAME_EXPERT_1", meeting["second_expert"]["first_name"])
    filedata = filedata.replace(
        "CONTACT.WSM___CONFIRMED_MEETING_DATE_AND_TIME",
        datetime.datetime.fromisoformat(meeting["second_expert"]["status"][0]["date"]).strftime(
            "%m/%d/%Y, %H:%M:%S, %Z"
        ),
    )
    filedata = filedata.replace("CONTACT.WSM___FULL_NAME_EXPERT_2", meeting["first_expert"]["name"])
    filedata = filedata.replace("CONTACT.WSM___EMAIL_ADDRESS_EXPERT_2", meeting["first_expert"]["email"])
    filedata = filedata.replace("CONTACT.WSM___FIRST_NAME_EXPERT_2", meeting["first_expert"]["first_name"])

    title = re.findall('"([^"]*)"', filedata.split('<meta property="og:title" content=')[1])[0]
    email = meeting["second_expert"]["email"]
    s2 = send_email(email, filedata, title)
    return (s1, s2)


def send_accept_meeting(meeting, expert1, expert2):
    # Read in the file
    with open(config.ROOT_DIR / "html_templates/accepted_status_meeting.html", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("CONTACT.WSM_FIRST_NAME_EXPERT_1", meeting[expert2]["first_name"])
    filedata = filedata.replace(
        "CONTACT.WSM___FIRST_PROPOSED_MEETING_INVITATION",
        datetime.datetime.fromisoformat(meeting[expert2]["status"][0]["date"]).strftime("%m/%d/%Y, %H:%M:%S, %Z"),
    )
    filedata = filedata.replace("CONTACT.WSM___FULL_NAME_EXPERT_2", meeting[expert1]["first_name"])

    title = re.findall('"([^"]*)"', filedata.split('<meta property="og:title" content=')[1])[0]
    email = meeting[expert2]["email"]
    s1 = send_email(email, filedata, title)
    return s1


def send_declined_meeting(meeting, expert1, expert2):
    # Read in the file
    with open(config.ROOT_DIR / "html_templates/decline_status_meeting.html", "r") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("CONTACT.WSM_FIRST_NAME_EXPERT_1", meeting[expert2]["first_name"])
    filedata = filedata.replace("CONTACT.WSM___FULL_NAME_EXPERT_2", meeting[expert1]["first_name"])

    title = re.findall('"([^"]*)"', filedata.split('<meta property="og:title" content=')[1])[0]
    email = meeting[expert2]["email"]
    s1 = send_email(email, filedata, title)
    return s1


def send_placeholder_email(email, times, first_name, tz):

    day_endings = {1: "st", 2: "nd", 3: "rd", 4: "th", 5: "th", 6: "th", 7: "th", 8: "th", 9: "th", 10: "th"}
    if not tz:
        return f"Email was not sent to {email} because there was no timezone"
    date_times_string = ""
    for ind, time_raw in enumerate(times):
        timeobj = pytz.utc.localize(datetime.datetime.fromisoformat(time_raw[:-1])).astimezone(pytz.timezone(tz))
        date_times_string = (
            date_times_string
            + "<b>"
            + str(ind + 1)
            + day_endings[ind + 1]
            + " | "
            + timeobj.strftime("%A, %B %e, %Y")
            + "</b>"
            + "<br>"
            + timeobj.strftime("%I:%M%p ").lower()
            + timeobj.strftime("%Z")
            + " ("
            + tz.replace("_", " ")
            + ") <br><br>"
        )

    # Read in the file
    with open(config.ROOT_DIR / "html_templates/email_placeholder.html", "r") as file:
        filedata = file.read()

    title = re.findall('"([^"]*)"', filedata.split('<meta property="og:title" content=')[1])[0]

    # Replace the target string
    filedata = filedata.replace("{{first_name}}", first_name)
    filedata = filedata.replace("{{testing_html}}", date_times_string)
    s1 = send_email(email, filedata, title)
    return s1
