from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.default import main_menu

from loader import dp,db,bot


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam",
            "/admin - Admin uchun buyruq")
    
    await message.answer("\n".join(text))
    
@dp.callback_query_handler(text='static')
async def bot_static(message: types.Message):
        users = db.users_count(1)
        male = db.male_count(1)
        female = db.female_count(0)
        await bot.delete_message(message.from_user.id,message.message.message_id)
        await bot.send_message(message.from_user.id,f"🎲Bot 📊Statistikasi:\n\n🙋‍♂️Erkaklar: {male}ta\n\n🙋‍♀️Ayollar: {female}ta\n\n✅Jami Faol Foydalanuvchilar: {users}ta")


        