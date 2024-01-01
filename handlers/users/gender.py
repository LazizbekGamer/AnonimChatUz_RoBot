from loader import dp,db
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command


@dp.message_handler(text="👥Jinsni o'zgartirish")
async def up_date_gender(message:types.Message):
    