import gspread
import requests
import slack
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])

sa = gspread.service_account(filename="gspread/service_account.json")
sh = sa.open("SeahorseUpdate")
wks = sh.worksheet("Sheet1")


clockInTimes = (wks.get("NQ18:NR27"))
inimesedKesOnPuhkusel = []

tahendused = {
    "V": "Vacation :palm_tree:",
    "jobi": "Jobistamas",
    "BH": "Bank Holiday :bank: :palm_tree: ",
    "CD": "Pipedrive Holiday",
    "LA": "Sick Leave :face_with_thermometer:",
}

peopleDictionary = {}
slackText = ""
nobody = ""

for [tahendus, inimene] in clockInTimes:
    peopleDictionary
    if tahendus.isnumeric() == False:
        eesnimi = inimene.split(".")[0].capitalize()
        slackText = slackText + eesnimi + " - " + tahendused[tahendus] + "\n"
        

if len(slackText) == 0:
    client.chat_postMessage(
channel='#api', text =":wave::skin-tone-4: Hello Seahorses!\nNobody's absent today, have a nice shift! :shteam:")

else:
    client.chat_postMessage(
    channel='#api', text ="Hello Seahorses! :shteam:\n\nPeople absent today:\n\n" + slackText + "\n\nHave a nice shift! :rocket: ")
  
