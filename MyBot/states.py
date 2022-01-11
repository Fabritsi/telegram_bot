from aiogram.dispatcher.filters.state import StatesGroup, State

class ReminderSettings(StatesGroup):
    TEXT = State()
    DATE = State()
    TIME = State()