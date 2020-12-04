import requests
import datetime
from time import sleep
import os

import pymongo
from dotenv import load_dotenv

from bothandler import BotHandler
from interact.register_user import Register


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
                chat_bot = Register(current_update["message"]["chat"]["id"], bot, db)
                print(current_update)
                if "chat" in current_update["message"]:
                    new_offset = current_update["update_id"]
                    print(new_offset)
                    if db["chats"].find_one({"chatId": current_update["message"]["chat"]["id"]}):
                        print("known chat")
                    else:
                        chat_bot.welcome()
        sleep(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()