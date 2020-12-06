import sys
from munch import munchify
sys.path.append('..')

# pylint: disable=import-error
from enums.messages import Messages
from enums.dbapi import Users
from enums.teleapi import Update
from messageHandler.adv_calendar import AdvCalendar

class MessageHandler:
    def __init__(self, chat_id, bot, db):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db

    #registrates new user and creates a document in database for the new user
    def welcome(self, a_message):
        self.bot.send_message(self.chat_id, Messages.WELCOME)
        result = self.db.users.insert_one({
            Users.CHAT_ID: self.chat_id,
            Users.NAME: a_message.chat.first_name,
            Users.REQUESTED_CALENDER: False,
            Users.HISTORY: [a_message.text],
            Users.ACCESSTRIES: 0,
            Users.CALENDAR: None
            })
        print(result)

    #registers the request for the collection
    def register_collection(self, requested_collection = ""):
        if self.db[requested_collection]:
            self.db.users.update_one({"chatId": self.chat_id}, { '$set': {Users.REQUESTED_CALENDER: requested_collection}})
            self.bot.send_message(self.chat_id, Messages.ASK_PASSCODE)
        else:
            self.bot.send_message(self.chat_id, Messages.NO_COLLECTION)

    def check_pass_code(self, a_message, a_user):
        if a_message.text == self.find_key_in_calendars("name", a_user.requestedCalendar).passcode:
            self.db.users.update_one({"chatId": self.chat_id}, {'$set': {"calendar": a_user.requestedCalendar}})
            self.bot.send_message(a_user.chatId, Messages.PASSCODE_ACCEPTED)
        else:
            self.db.users.update_one({Users.CHAT_ID: a_user.chatId}, {'$inc': {Users.ACCESSTRIES: 1}})
            self.bot.send_message(self.chat_id, "wrong passcode")
    
    def find_key_in_calendars(self, key, value):
        calendars = munchify(self.db.config.find_one({"name": "calendars"})).calendars
        for x in calendars:
            if x[key] == value:
                return x
        return None

    def recieved_message(self, a_message, a_user):
        if not a_user.calendar:
            if not a_user.requestedCalendar:
                if self.find_key_in_calendars("name", a_message.text):
                    self.register_collection(a_message.text)
                else:
                    self.bot.send_message(a_user.chatId, "Dieser Kalender ist nicht vorhanden, hast du dich vielleicht vertippt?")
            elif a_user.accessTries > 3:
                self.bot.send_message("too many tries. please try again later (20 min)")
            elif a_message.text == "cancel":
                print("todo: implement cancel")
            else:       #check passcode
                self.check_pass_code(a_message, a_user)                
        else:
            self.bot.send_message(self.chat_id, "Du hast schon einen Kalender, das reicht erstmal :)")
            AdvCalendar(self.chat_id, self.bot, self.db).run()
