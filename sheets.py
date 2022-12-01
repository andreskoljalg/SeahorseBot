import gspread
import requests
import slack
from dotenv import load_dotenv
from pathlib import Path
import os
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

sa = gspread.service_account(filename="gspread/service_account.json")
sh = sa.open("SeahorseUpdate")
wks = sh.worksheet("Sheet1")
marian = (wks.get("NQ18:NR18"))[0]
eden = (wks.get("NQ19:NR19"))[0] 
andres = (wks.get("NQ20:NR20"))[0]
aile = (wks.get("NQ21:NR21"))[0]
aire = (wks.get("NQ22:NR22"))[0]
tony = (wks.get("NQ23:NR23"))[0]
pavel = (wks.get("NQ24:NR24"))[0]
quinn = (wks.get("NQ25:NR25"))[0]
danita = (wks.get("NQ26:NR26"))[0]
relika = (wks.get("NQ27:NR27"))[0]

listnumbers = [marian[0], eden[0], andres[0], aile[0], aire[0], tony[0], pavel[0], quinn[0], danita[0], relika[0]]
if listnumbers[0:8]: "v"
listnumbers[0:8] = "vacation"
listnames = [marian[1], eden[1], andres[1], aile[1], aire[1], tony[1], pavel[1], quinn[1], danita[1], relika[1]]
#print(*listnumbers, sep="\n")
#print(*listnames, sep="\n")

message = listnumbers, listnames

client.chat_postMessage(channel='#api', text=message)


# If [0][0] = V
    # [0][0] = "Vacation"
#if andres[0][0] == "8":
 #   andres[0][0] = "su ema"

# Kuidas ma saan list1'te ainult nimi[0][0] valued?

#andres[0][1] = "@andres "
#print(andres[0][1], end="")
#print(andres[0][0])
