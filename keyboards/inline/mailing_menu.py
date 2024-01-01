from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

static = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📊Satistika',callback_data='static')
        ]
    ]
)