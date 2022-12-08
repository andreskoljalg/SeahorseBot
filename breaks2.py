    #V8 with improvements to pulling only the specific dated sheets
    #Getting the agent name from slack via API without the dictionary
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
from slack_sdk import WebClient
import datetime

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

sheetToRequest = datetime.datetime.now()
month = sheetToRequest.strftime("%b %-d")

sa = gspread.service_account(filename="gspread/service_account.json")
sh = sa.open("SeahorseUpdate")
wks = sh.worksheet(month)

SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

app = App(token=SLACK_BOT_TOKEN, name="Seahorse bot")
logging.basicConfig(level=logging.DEBUG)
say = ""
user_id = ""
@app.message(re.compile("^breaks$"))
def send_break_values(message, say, logger, body):
    channel_type = message["channel_type"]
    if channel_type != "im":
        return 0
    dm_channel = message["channel"]
    user_id = message["user"]
    text = "breaks"
    logger.info(f"{user_id} just saatis sõnumi ja ma saatsin vastu {text}")


    # Slack ID'd on juba dictionarys sees, nüüd oleks vaja lihtsalt alt
    # saada see [user_id] üles realt 71
    requestedRow = client.users_profile_get(user = user_id)["profile"]["real_name"]
    #print("\n\n\n" + requestedRow + "\n\n\n")
    requestingAgent = (wks.findall(requestedRow))
    logger.info(f"\n\n\nRequested row:{requestedRow}\nRequesting Agent: {requestingAgent}\n\n\n")

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