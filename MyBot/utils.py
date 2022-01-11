from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# keyboards

back_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('В головне меню'))

def list_keyboard(params):
    list_markup = InlineKeyboardMarkup()
    for par in params:
        list_markup.add(InlineKeyboardButton(f"{' '.join(par['text'].split(' ')[0:2])}...", callback_data=f"reminder:{params.index(par)}"))
    return list_markup

def reminder_card_keyboard(reminder_id):
    reminder_card_markup = InlineKeyboardMarkup()
    delete_btn = InlineKeyboardButton('Видалити', callback_data=f'delete:{reminder_id}')
    reminder_card_markup.add(delete_btn)
    return reminder_card_markup

menu_markup = InlineKeyboardMarkup()
create_btn = InlineKeyboardButton('Створити нагадування', callback_data='create')
list_btn = InlineKeyboardButton('Список нагадувань', callback_data='list')
menu_markup.add(create_btn)
menu_markup.add(list_btn)

# messages

messages = {
    "start_message" : "Бот-нагадувач.\n\nВ цьому боті ви можете створювати та оперувати нагадуваннями про певні події",
    "menu_message" : "<b>Меню</b>",
    "get_reminder_text_message" : "Введіть текст нагадування",
    "get_reminder_data" : "Виберіть дату нагадування",
    "get_reminder_time" : "Введіть час нагадування",
    "expire_date_error" : "Невірно вибрана дата. Виберіть майбутню дату",
    "success_create" : "Нагадування створено!",
    "expire_time_error" : "Введіть коректно час",
    "list_menu" : "<b>Виберіть нагадування зі списку</b>"
}

