from aiogram.dispatcher.filters.state import State,StatesGroup

class bot_mailing_photo(StatesGroup):
    photo_text = State()
    photo = State()