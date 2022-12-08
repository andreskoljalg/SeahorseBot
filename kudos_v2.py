import gspread
import requests
import slack
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
import os
import logging
import re
from slackeventsapi import SlackEventAdapter
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App
from datetime import datetime
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
app = App(token=SLACK_BOT_TOKEN, name="Seahorse bot")

sa = gspread.service_account(filename="gspread/service_account.json")
sh = sa.open("SeahorseUpdate")
wks = sh.worksheet("kudos")
logging.basicConfig(level=logging.DEBUG)

@app.message(re.compile("^props"))
def KudosBot(message, say, logger, body):
    logger.info(f"request body: {body}")
    print(body)

    channel_type = message["channel_type"]
    if channel_type != "im":
        return 0
    dm_channel = message["channel"]
    user_id = message["user"]
    kudosID = message["text"][8:19]
    logger.info(f"***LOGGER BEFORE userID4Logging\n{user_id}")
    userID4Logging = client.users_profile_get(user = user_id)["profile"]["real_name"]
    kudosReceiverName = client.users_profile_get(user = kudosID)["profile"]["real_name"]
    logger.info(f"***LOGGER AFTER userID4Logging***\nuser_id:{user_id}\nuserID4Logging:{userID4Logging}")
    if user_id == kudosID:
        say(text="Nice try, but you cannot kudos yourself.", channel=dm_channel)
        logger.info(f"{userID4Logging} just proovis iseendale propsi visata!")
        return 0

    else:
        say(text="Thanks! Kudos Submitted.", channel=dm_channel)
        logger.info(f"\nKudos ID: {kudosID}\nUser ID: {user_id}\n")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        wks.append_row([kudosReceiverName, current_time, userID4Logging], table_range="A2")
        logger.info(f"{userID4Logging} just viskas propsi kasutajale {kudosReceiverName}")
        return 0

def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()