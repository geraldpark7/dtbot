import os
import logging
import random

import schedule as schedule
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi
from dtbotmessage import DTBotMessage

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ["SLACK_SIGNING_SECRET"], "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# For simplicity we'll store our app data in-memory with the following data structure.
# onboarding_tutorials_sent = {"channel": {"user_id": OnboardingTutorial}}
onboarding_tutorials_sent = {}
dtbot_channel = ""
channel_members = set()

def refresh_members(channel):
    dtbot_channel = channel
    channel_members = set(slack_web_client.conversations_members(channel))
    # Remove staff
    channel_members.remove()
    channel_members.remove()

def assign_dt():
    assignees = list()
    for i in range(3):
        random_user_id = random.sample(channel_members, 1)[0]
        assignees.append(slack_web_client.users_info(random_user_id)['real_name'])
        channel_members.remove(random_user_id)
    assignees.sort()
    post_dtbot_msg(dtbot_channel, assignees)


def post_dtbot_msg(channel: str, assignees: list):
    # Create a new onboarding tutorial.
    dtbot = DTBotMessage(channel, assignees)

    # Get the onboarding message payload
    message = dtbot.get_message_payload()

    # Post the onboarding message in Slack
    response = slack_web_client.chat_postMessage(**message)

# Weekly Scheduler
schedule.every().sunday.at("07:00").do(refresh_members("sophbros-dt"))
schedule.every().monday.at("07:00").do(assign_dt())
schedule.every().wednesday.at("07:00").do(assign_dt())
schedule.every().friday.at("07:00").do(assign_dt())

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    app.run()
