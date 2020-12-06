from datetime import date, timedelta

class AdvCalendar:
    def __init__(self, chat_id, bot, db):
        self.chat_id = chat_id
        self.bot = bot
        self.db = db
        self.advent = [date(date.today().year, 12, 1) + timedelta(days = delta_day) for delta_day in range(24) ]
        print("advent: ", self.advent)

    def is_advent_time(self, a_day):
        if a_day in self.advent:
            print("todo")
            
    def new_day(self):
        print("new day")

    def run(self):
        if date.today() in self.advent:
            self.bot.send_message(self.chat_id, "es ist advent")
            print("todo")