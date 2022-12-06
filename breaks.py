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
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

sa = gspread.service_account(filename="gspread/service_account.json")
sh = sa.open("SeahorseUpdate")
wks = sh.worksheet("Sheet2")

slackIDtoName = {
   "U0490624DBR": "Andres Kõljalg",
   "U02J98XN623": "Aile Parve",
   "U02JH7HGDD4": "Aire Randalu",
   "U0490624DBR": "Danita Siik",
   "U03LP6QRZ0A": "Eden Sicat",
   "U038FGDP6R4": "Marian Luht",
   "U03CHMJ0QMQ": "Pavel Provotorov",
   "U03283YUV3R": "Quinn Feller",
   "U032NMX5UDQ": "Relika Susi",
   "U032NMX9MGS": "Tony Xavier"
}

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

app = App(token=SLACK_BOT_TOKEN, name="Seahorse bot")
logging.basicConfig(level=logging.DEBUG)
say = ""
user_id = ""
@app.message(re.compile("^breaks$"))
def send_break_values(message, say, logger, body):
    #logger.info(f"request body: {body}")
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    dm_channel = message["channel"]
    user_id = message["user"]
    text = "breaks"
    logger.info(f"{user_id} just saatis sõnumi ja ma saatsin vastu {text}")

    # Slack ID'd on juba dictionarys sees, nüüd oleks vaja lihtsalt alt
    # saada see [user_id] üles realt 71
    requestingAgent = (wks.findall(slackIDtoName[user_id]))

    # Giving "Aire Randalu" just for testing
    #requestingAgent = (wks.findall("Aire Randalu"))
    requestingAgentRow = requestingAgent[0].row

    requestedRow = requestingAgent[0]

    getRange = 'H'+ str(requestingAgentRow) +':AJ'+ str(requestingAgentRow)
    agentTimeline = (wks.range(getRange))

    tallinnTimeline = (wks.get("H1:AJ1"))[0]

    conditions = ["break", "away"]
    slackText = ''
    for breakvalue in agentTimeline:
        if breakvalue.value == 'break' or breakvalue.value == 'away':
            columnOffset = breakvalue.col - 8
            
            slackText = slackText + breakvalue.value +' '+ tallinnTimeline[columnOffset][:5] +"\n"

    slackTextEdited = "Hello! :wave:\nHere are your breaks for today:\n" + slackText + "\nHave a nice shift! :rocket:"
    print(slackTextEdited)


    say(text=slackTextEdited, channel=dm_channel)

def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()

