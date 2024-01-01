from aiogram.dispatcher.filters.state import State,StatesGroup

class set_balance(StatesGroup):
    chat_id = State()

class get_new_balance(StatesGroup):
    balance = State()
    chat_id = State()

class rm_balance(StatesGroup):
    chat_id = State()
    amount = State()

class get_rm_balance(StatesGroup):
    amount = State()
    chat_id = State()

class get_balance(StatesGroup):
    chat_id = State()
