import requests
import datetime
from time import sleep
import os

import pymongo
from dotenv import load_dotenv

from bothandler import BotHandler
from interact.register_user import Register

from enums.dbapi import Collections, Adventskalender, Users
from enums.teleapi import Update
from enums.messages import Messages

load_dotenv()

token = os.environ.get('TELEGRAM-TOKEN')
bot = BotHandler(token)
db = pymongo.MongoClient(os.environ.get("MONGO-LINK"))["Adventskalender"]


def main():
    new_offset = 0
    print('now launching...')

    while True:
        all_updates = bot.get_updates(new_offset)
        print(all_updates)

        if len(all_updates) > 0:
            for current_update in all_updates:
                current_chat_id = current_update["message"]["chat"]["id"]
                current_user = db[Collections.USERS].find_one({Users.CHAT_ID: current_chat_id})
                current_text = current_update["message"]["chat"]["id"]
                current_date = current_update[Update.MESSAGE][Update.DATE]

                chat_bot = Register(current_chat_id, bot, db)

                print(current_update)
                if "chat" in current_update["message"]:
                    new_offset = current_update["update_id"]
                    print(new_offset)
                    # check if chatId is known in database
                    if db[Collections.USERS].find_one({Users.CHAT_ID: current_chat_id}):
                        print("known chat")
                        #todo datenbank akrtualisieren
                        #todo add accesstries in if below
                        if current_user[Users.REQUESTED_CALENDER]:
                            print("hallo")
                            #todo datenbank abfragen, welcher kalender requested wurde --> den passcode vom kalender mit der eingegebenen nachricht vergleichen.
                            #if failed db erweitern um passcodeversuch
                            
                    else:
                        chat_bot.welcome(current_update[Update.MESSAGE])
        sleep(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()