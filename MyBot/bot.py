from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from datetime import datetime, date, time

import configparser

from utils import *
from states import *
from dbase import DBase

config = configparser.ConfigParser()
config.read("config.ini")

bot = Bot(token=config["Bot"]["token"], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

db = DBase()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if db.get_user_object(message.chat.id) == None:
        db.add_new_user(message.chat.id)

    await bot.send_message(message.chat.id, messages["start_message"], reply_markup=back_markup)
    await bot.send_message(message.chat.id, messages["menu_message"], reply_markup=menu_markup)

@dp.message_handler(lambda msg: msg.text == 'В головне меню', state="*")
async def go_to_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, messages["menu_message"], reply_markup=menu_markup)

@dp.callback_query_handler(lambda c: c.data == 'create', state=None)
async def process_callback_create_btn(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, messages["get_reminder_text_message"])
    await ReminderSettings.TEXT.set()

@dp.callback_query_handler(lambda c: c.data == 'list', state=None)
async def process_callback_create_btn(callback_query: types.CallbackQuery):
    user_object = db.get_user_object(callback_query.from_user.id)

    await bot.send_message(callback_query.from_user.id, messages["list_menu"], reply_markup=list_keyboard(user_object["reminders"]))

@dp.callback_query_handler(lambda c: c.data.startswith("reminder"), state=None)
async def get_reminder_card(callback_query: types.CallbackQuery):
    user_object = db.get_user_object(callback_query.from_user.id)
    reminder_id = int(callback_query.data.split(":")[-1])
    
    reminder_text = user_object["reminders"][reminder_id]["text"]
    reminder_date = datetime.fromtimestamp(user_object["reminders"][reminder_id]["timestamp"])

    reminder_card_text = f'{reminder_text}\n\n{reminder_date.strftime("%m/%d/%Y, %H:%M:%S")}'

    await bot.send_message(callback_query.from_user.id, reminder_card_text, reply_markup=reminder_card_keyboard(reminder_id))

@dp.callback_query_handler(lambda c: c.data.startswith("delete"), state=None)
async def get_reminder_card(callback_query: types.CallbackQuery):
    user_object = db.get_user_object(callback_query.from_user.id)
    reminder_id = int(callback_query.data.split(":")[-1])

    db.delete_reminder(callback_query.from_user.id, reminder_id)

    await bot.send_message(callback_query.from_user.id, messages["menu_message"], reply_markup=menu_markup)

@dp.message_handler(state=ReminderSettings.TEXT)
async def get_reminder_text(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "text" : message.text
        }
    )
    await bot.send_message(message.from_user.id, messages["get_reminder_data"], reply_markup=await SimpleCalendar().start_calendar())
    await ReminderSettings.DATE.set()

@dp.callback_query_handler(simple_cal_callback.filter(), state=ReminderSettings.DATE)
async def get_reminder_expire_date(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, set_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    now_date = datetime.now()
    
    if set_date:
        if now_date <= set_date or now_date.strftime("%Y/%m/%d") == set_date.strftime("%Y/%m/%d"):
            await state.update_data(
                {
                    "expire_date": set_date.strftime("%d/%m/%Y")
                }
            )

            await bot.send_message(callback_query.from_user.id, f"Ви вибрали {set_date.strftime('%d/%m/%Y')}")
            await bot.send_message(callback_query.from_user.id, messages["get_reminder_time"])
            await ReminderSettings.TIME.set()
        else:
            await bot.send_message(callback_query.from_user.id, messages["expire_date_error"])
            await bot.send_message(callback_query.from_user.id, messages["get_reminder_data"], reply_markup=await SimpleCalendar().start_calendar())
            await ReminderSettings.DATE.set()

@dp.message_handler(state=ReminderSettings.TIME)
async def get_reminder_expire_time(message: types.Message, state: FSMContext):
    await state.update_data(
        {
            "time" : message.text
        }
    )
    state_data = await state.get_data()

    try:
        datetime_expire_obj = datetime.strptime(state_data['expire_date'] + " " + state_data['time'], "%d/%m/%Y %H %M")

        reminder_object = {
            "text" : state_data["text"],
            "timestamp" : datetime.timestamp(datetime_expire_obj)
        }

        db.add_new_reminder(message.from_user.id, reminder_object)

        await state.finish()
        await bot.send_message(message.from_user.id, messages["success_create"])
        await bot.send_message(message.chat.id, messages["menu_message"], reply_markup=menu_markup)

    except:
        await bot.send_message(message.from_user.id, messages["expire_time_error"])
        await ReminderSettings.TIME.set()


if __name__ == '__main__':
    executor.start_polling(dp)