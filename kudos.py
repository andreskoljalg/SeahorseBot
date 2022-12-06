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

slackIDtoName = {
   "<@U0490624DBR>": "Andres Kõljalg",
   "<@U04E10C3DR9>": "+1SlackTest",
   "<@U04E13XQ4JE>": "2SlackTest",
   "<@U02J98XN623>": "Aile Parve",
   "<@U02JH7HGDD4>": "Aire Randalu",
   "<@0490624DBR>": "Danita Siik",
   "<@U03LP6QRZ0A>": "Eden Sicat",
   "<@U038FGDP6R4>": "Marian Luht",
   "<@U03CHMJ0QMQ>": "Pavel Provotorov",
   "<@U03283YUV3R>": "Quinn Feller",
   "<@U032NMX5UDQ>": "Relika Susi",
   "<@U032NMX9MGS>": "Tony Xavier"
}
startCellOne = 1
startCellTwo = 1
inputText = ""
logging.basicConfig(level=logging.DEBUG)

@app.message(re.compile("^props"))
def KudosBot(message, say, logger, body):
    logger.info(f"request body: {body}")
    print(body)

    channel_type = message["channel_type"]
    if channel_type != "im":
        return

    dm_channel = message["channel"]
    user_id = message["user"]
    kudosID = message["text"][8:19]
    rawText = message["text"][6:]
    userID2Name = "<@" + user_id + ">"
    userID4Logging = (slackIDtoName[userID2Name])
    inputText = (slackIDtoName[rawText])

    if user_id == kudosID:
        say(text="Nice try, but you cannot kudos yourself.", channel=dm_channel)
        logger.info(f"{user_id} just proovis iseendale propsi visata!")
        return 0

    else:
        say(text="Thanks! Kudos Submitted.", channel=dm_channel)
        logger.info(f"\nKudos ID: {kudosID}\nUser ID: {user_id}\n")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        wks.append_row([inputText, current_time, userID4Logging], table_range="A2")
        logger.info(f"{userID4Logging} just viskas propsi kasutajale {inputText}")
        return 0


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()