import sys
import os
sys.path.append('..')

# pylint: disable=import-error
from enums.messages import Messages
from enums.dbapi import Users
from enums.teleapi import Update

class Register:
    def __init__(self, chat_id, bot, db):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db

    #registrates new user and creates a document in database for the new user
    def welcome(self, a_message):
        self.bot.send_message(self.chat_id, Messages.WELCOME)
        self.db["chats"].insert_one({
            Users.CHAT_ID: self.chat_id,
            Users.NAME: a_message[Update.CHAT][Update.FIRST_NAME],
            Users.REQUESTED_CALENDER: False,
            Users.HISTORY: [a_message[Update.CHAT][Update.TEXT]]
            })

    #registers the request for the collection
    def register_collection(self, requested_collection = ""):
        if self.db[requested_collection]:
            self.db["chats"].update_one({"chatId": self.chat_id}, {"requestedCollection": requested_collection})
            self.bot.send_message(self.chat_id, Messages.ASK_PASSCODE)
        else:
            self.bot.send_message(self.chat_id, Messages.NO_COLLECTION)