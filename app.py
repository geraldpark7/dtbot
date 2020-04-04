import os
import random
import schedule
import time
import logging

from slack import WebClient
from dtassignment import DTassignment

logging.basicConfig(level=logging.DEBUG)


def get_channel_members_and_sanitize(channel: str) -> set:
    members = slack_web_client.conversations_members(
        channel=channel
    )
    if members['ok'] is not True:
        logging.error(members)

    slack_members = set(members['members'])

    # Remove DT Bot
    if 'U010M5E8CAE' in slack_members:
        slack_members.remove('U010M5E8CAE')
    # Remove the staff
    if 'U0111P7L7FY' in slack_members:
        slack_members.remove('U0111P7L7FY')  # Remove Gerald Park
    if 'U010ZT6TALD' in slack_members:
        slack_members.remove('U010ZT6TALD')  # Remove Johnny Yeo

    return slack_members


def dtbot_post_weekly_msg(dt_assignment: DTassignment) -> None:
    def msg(greeting: int) -> str:
        switcher = {
            1: "HALLELUJAH :sunny: God said Let there be DT !!!",
            2: "ATTENTION Y\'ALL.. this is the DT groups!",
            3: "I said \"YO GOD, WHAT BE THE DT GROUPS DIS WEEK?\" :thinking_face:",
        }
        return switcher.get(greeting, "Invalid option")

    welcoming_greeting = msg(random.randint(1,3))
    ending_greeting = "Happy Sunday y\'all!! :smile:"

    # Post the intro message in Slack
    sendMessage(welcoming_greeting)
    sendMessage("Monday DT group is: " + dt_assignment.mon_grouping())
    sendMessage("Wednesday DT group is: " + dt_assignment.wed_grouping())
    sendMessage("Friday DT group is: " + dt_assignment.fri_grouping())
    sendMessage(ending_greeting)


def dtbot_post_msg(grouping: str) -> None:
    def msg(greeting: int) -> str:
        switcher = {
            1: "Morning ya shmucks! :sunny: God said the DT group for today is ... :thinking_face:",
            2: "Rise & Shine lil boys! :sunny: God said the DT group for today is ... :thinking_face:",
            3: "WAKE UP KIDZ! :sunny: God said the DT group for today is ... :thinking_face:",
        }
        return switcher.get(greeting, "Invalid option")

    welcoming_greeting = msg(random.randint(1,3))
    ending_reminder = "Remember to post on slack, the passage you read and what you got out of DT! :smile:"

    # Post the intro message in Slack
    sendMessage(welcoming_greeting)
    sendMessage(grouping)
    sendMessage(ending_reminder)


def sendMessage(msg):
    updateMsg = slack_web_client.chat_postMessage(
        channel=dtbot_channel,
        text=msg
    )
    # check if the request was a success
    if updateMsg['ok'] is not True:
        logging.error(updateMsg)
    else:
        logging.debug(updateMsg)


def refresh_schedule(dt_assignment: DTassignment) -> None:
    dt_assignment.clear_groupings()
    dt_assignment.assign_random_groupings()


if __name__ == "__main__":
    # Initialize a Web API client
    slack_web_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    logging.debug("Authorized Slack Client")

    # Initialize Slack variables
    dtbot_channel = 'G010MA06WBU'
    # testing-private-channel id = G010QH1D0M7
    # sophbros-dt id = G010MA06WBU

    channel_members = get_channel_members_and_sanitize(dtbot_channel)
    dt_assignment = DTassignment(channel_members)
    dt_assignment.assign_random_groupings()

    # times are in UTC
    schedule.every().sunday.at("14:00").do(lambda: dtbot_post_weekly_msg(dt_assignment))  # weekly dt group announcement

    schedule.every().monday.at("14:00").do(lambda: dtbot_post_msg(dt_assignment.mon_grouping()))

    schedule.every().tuesday.at("14:00").do(lambda: dtbot_post_msg(":smiley: <@U010ZT6TALD> :smiley:"))  # assign DT to JY

    schedule.every().wednesday.at("14:00").do(lambda: dtbot_post_msg(dt_assignment.wed_grouping()))

    schedule.every().thursday.at("14:00").do(lambda: dtbot_post_msg(":smirk: <@U0111P7L7FY> :smirk:"))  # assign DT to GP

    schedule.every().friday.at("14:00").do(lambda: dtbot_post_msg(dt_assignment.fri_grouping()))

    schedule.every().saturday.at("14:00").do(lambda: refresh_schedule(dt_assignment))

    while True:
        schedule.run_pending()
        time.sleep(50)  # sleep for 50 seconds between checks on the scheduler
