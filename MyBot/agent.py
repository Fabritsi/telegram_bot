import telebot
import configparser

from dbase import DBase
from datetime import datetime

config = configparser.ConfigParser()
config.read("config.ini")

db = DBase()
bot = telebot.TeleBot(config["Bot"]["token"], parse_mode=None)

print("Agent start!")

while True:

    all_users = db.get_all_users()

    for user in all_users:
        print(f"Check user with id {user['id']}")
        user_reminders = user["reminders"]
        for reminder in user_reminders:
            if reminder["timestamp"] <= datetime.timestamp(datetime.now()):
                bot.send_message(user["id"], reminder["text"])
                user_reminders.remove(reminder)
                db.update_reminders_list(user["id"], user_reminders)

print("Agent stop!")
