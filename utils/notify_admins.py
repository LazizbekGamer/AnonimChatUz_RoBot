import sqlite3
from loader import bot, dp
from aiogram import types
from data.config import *

async def on_start_notify(dp):
    for admin_id in ADMINS:
        try:
            message = "<b>💠 Bot qayta ishga tushirildi! \n🔄 Yangilash uchun \n<u>\t/start /start /start /start</u></b>"
            await bot.send_message(
                admin_id,
                message,
                parse_mode=types.ParseMode.HTML
            )
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")

async def on_shutdown_notify(dp):
    for admin_id in ADMINS:
        try:
            message = "<b>🛑 Bot vaqtinchalik to'xtatildi‼️\n🕒 Tez orada qayta ishga tushiriladi</b>"
            await bot.send_message(
                admin_id,
                message,
                parse_mode=types.ParseMode.HTML
            )
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")
