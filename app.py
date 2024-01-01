import os
import asyncio
from aiogram import executor, types
from loader import dp, bot, db
import middlewares, filters, handlers
from utils.on_startup import on_startup
from utils.on_shutdown import on_shutdown
from utils.create_tables import create_table_start



os.system("clear && clear")
print("""
\n
\033[92m\033[1m╔╗──────────────╔╗────╔╗─╔═══╗
\033[92m\033[1m║║──────────────║║────║║─╚╗╔╗║
\033[92m\033[1m║║──╔══╦═══╦╦═══╣╚═╦══╣║╔╗║║║╠══╦╗╔╗
\033[92m\033[1m║║─╔╣╔╗╠══║╠╬══║║╔╗║║═╣╚╝╝║║║║║═╣╚╝║
\033[92m\033[1m║╚═╝║╔╗║║══╣║║══╣╚╝║║═╣╔╗╦╝╚╝║║═╬╗╔╝
\033[92m\033[1m╚═══╩╝╚╩═══╩╩═══╩══╩══╩╝╚╩═══╩══╝╚╝
\n\n\n\033[91m\033[1mThe bot is starting up...\n
\033[94mPlease wait...\033[0m\033[1m\n
\033[91mSkipped all updates...\033[92m\033[1m
""")



@dp.chat_member_handler()
async def chat_memberupdate(message: types.ChatMemberUpdated):
    try:
        old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "left":
            await bot.send_message(new.user.id, "<i>❌ Siz ba'zi kanallarimizdan chiqib ketdingiz!\nIltimos qaytadan kanalga obuna bo'ling va chiqib ketmang ❗️\n\nAks holda botimizdan foydalana olmaysiz</i>")
    except:
        pass




if __name__ == '__main__':
    try:
        create_table_start(dp)
        db.update_custom_balance()
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True, allowed_updates=types.AllowedUpdates.all())
    except TimeoutError:
        pass
    except KeyboardInterrupt as e:
        print("\n\033[93m\033[1mDastur tuxtatildi!\033[0m\n")
        pass
    #except Exception as e:
       # print(e)