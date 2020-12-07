import requests
import datetime
from time import sleep
import os
import sys
from munch import munchify

import pymongo
from dotenv import load_dotenv

from bothandler import BotHandler
from messageHandler.message_handler import MessageHandler
from messageHandler.adv_calendar import AdvCalendar

from enums.dbapi import Users, Collections, Adventskalender, Config
from enums.teleapi import Update
from enums.messages import Messages

load_dotenv()

token = os.environ.get('TELEGRAM-TOKEN')
bot = BotHandler(token)
db = pymongo.MongoClient(os.environ.get("MONGO-LINK")).Adventskalender


def main():
    new_offset = db.config.find_one({"name": "offset"})["offset"]
    print('now launching...')

    while True:
        # run adv calendar
        for user_dict in db.users.find():
            adv_cal = AdvCalendar(user_dict[Users.CHAT_ID], bot, db)
            adv_cal.run()
        all_updates = bot.get_updates(new_offset)
        print("all updates", all_updates, new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                update = munchify(current_update)
                print("update text: ", update.message.text)
                current_chat_id = munchify(update.message.chat.id)
                current_user = munchify(db.users.find_one({"chatId": current_chat_id}))
                # current_text = current_update["message"]["chat"]["id"]
                # current_date = current_update[Update.MESSAGE][Update.DATE]

                message_handler = MessageHandler(current_chat_id, bot, db)

                print(current_update)
                if Update.CHAT in update.message:
                    new_offset = update.update_id + 1
                    db.config.find_one_and_update({"name": "offset"}, {'$set': {'offset': new_offset}})
                    print(new_offset)
                    # check if chatId is known in database
                    user = munchify(db.users.find_one({Users.CHAT_ID: current_chat_id}))
                    if user:
                        message_handler.recieved_message(munchify(update.message), current_user)
                        bot.send_message(current_chat_id, update.message.text)
                        print("known chat")
                        
                        #todo datenbank akrtualisieren
                        #todo add accesstries in if below
                        # if not current_user.requestedCalendar and not current_user.calendar:
                        #     print("todo or not")
                        # if current_user[Users.REQUESTED_CALENDER]:
                        #     print("hallo")
                        #     #todo datenbank abfragen, welcher kalender requested wurde -- den passcode vom kalender mit der eingegebenen nachricht vergleichen.
                        #     #if failed db erweitern um passcodeversuch
                        
                    else:
                        print("unknown chat")
                        message_handler.welcome(update.message)
        sleep(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()