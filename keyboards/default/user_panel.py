import re
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🫂 Suxbatdosh izlash")
        ],
        [
            KeyboardButton(text="🤴 O'g'il bola"),
            KeyboardButton(text="👸 Qiz bola")
        ],
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text='📚Bot Haqida')
        ]
    ],resize_keyboard=True
)

stop_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Qidiruvni To'xtatish")
        ]
    ],resize_keyboard=True
)


stop_chat_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌Chatni To'xtatish")
        ]
    ],resize_keyboard=True
)

check_gender_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("👨 Ogil bola"),
            KeyboardButton("👩 Qiz bola")
        ]
    ],resize_keyboard=True
)

search_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🤴 O'g'il bola"),
            KeyboardButton(text="👸 Qiz bola"),
            KeyboardButton("👬Random")
        ],
        [
            KeyboardButton(text="🔝Bosh Menuga Qaytish")
        ]
    ],resize_keyboard=True
)

