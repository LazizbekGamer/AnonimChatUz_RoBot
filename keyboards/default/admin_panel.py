import re
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

admin_menu=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💰Pul-qoshish"),
            KeyboardButton(text="💰Pul-ayirish")
        ],
        [
            KeyboardButton(text="💰Pul-aniqlash")
        ],
        [
            KeyboardButton(text="👤 Userlar Ruyhati")
        ],
        [
            KeyboardButton(text='📊Statistika'),
            KeyboardButton(text='📤Xabar')
        ]
    ],resize_keyboard=True
)

mailing_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌠Rasmli Xabar Yuborish"),
            KeyboardButton(text='⌨️Matnli Xabar Yuborish')
        ]
    ],resize_keyboard=True
)