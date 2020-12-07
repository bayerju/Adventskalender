import sys
from munch import munchify
sys.path.append('..')

# pylint: disable=import-error
from datetime import date, timedelta, datetime
from enums.dbapi import Users

class AdvCalendar:
    def __init__(self, chat_id, bot, db):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db
        self.user = munchify(db.users.find_one({Users.CHAT_ID: chat_id}))
        self.calendar = db[self.user.calendar] if self.user.calendar else None
        self.advent = [date(date.today().year, 12, 1) + timedelta(days = delta_day) for delta_day in range(24) ]
        print("advent: ", self.advent)

    def is_advent_time(self, a_day):
        if a_day in self.advent:
            print("todo")

    def send_adv_message(self):
        self.bot.send_message(self.chat_id, "adv message with button")

    def run(self):
        print("Calendar is running")
        if date.today() in self.advent and self.user.calendar and self.user.lastSentAdvMessage.date() != date.today():
            self.send_adv_message()
            self.db.users.update_one({
                Users.CHAT_ID: self.chat_id},
                {'$set': {Users.LAST_SENT_ADV_MESSAGE: datetime.now()}
                })
            print("todo")