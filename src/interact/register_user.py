import sys
import os
sys.path.append('..')

from enums.messages import Messages

class Register:
    def __init__(self, chat_id, bot, db):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db

    #registrates new user and creates a document in database for the new user
    def welcome(self):
        self.bot.send_message(self.chat_id, Messages.WELCOME)
        self.db["chats"].insert_one({"chatId": self.chat_id})

    def register_collection(self, requested_collection = ""):
        if self.db[requested_collection]:
            self.db["chats"].update_one({"chatId": self.chat_id}, {"requestedCollection": requested_collection})
            self.bot.send_message(self.chat_id, Messages.ASK_PASSCODE)
        else:
            self.bot.send_message(self.chat_id, Messages.NO_COLLECTION)