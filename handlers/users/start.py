from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import main_menu,check_gender_menu
from loader import dp,db,bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, Message
from keyboards.default import stop_menu, main_menu, stop_chat_menu,search_menu
from aiogram.dispatcher.filters import Command
from keyboards.inline import static
from data import config
import asyncio






class Change_Age(StatesGroup):
    get_for_age = State()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info == None or False:
        pass
    else:
        db.delate_chats(chat_info[0])
    if not db.user_exists(message.from_user.id,'1'or'0'):
        await message.answer(f"👋 Salom, <b>{message.from_user.full_name}</b>\n 👇Pastdagi tugmalar orqali jinsingizni tanlang!\n⁉️ Agarda botdan foydalana olmasangiz adminga murojaat qiling...\n👨🏻‍💻 Admin bilan bog'lanish: {config.ADMIN}", reply_markup=check_gender_menu)
        
        
    else:  
        await message.answer(f"👋 Salom, <b>{message.from_user.full_name}</b> \n👇Pastdagi tugmalar orqali botdan foydalaning...\n⁉️ Agarda botdan foydalana olmasangiz adminga murojaat qiling...\n👨🏻‍💻 Admin bilan bog'lanish: {config.ADMIN}", reply_markup=main_menu)
        
    

@dp.message_handler(text='👨 Ogil bola')
async def set_gender(message:types.Message):
    if db.set_gender(message.from_user.id,'1'):
        db.add_balance(message.chat.id, config.DAILY_LIMIT)
        await asyncio.sleep(0.2)
        age = db.get_age(message.chat.id)
        if age == 0:
            msg_get_age = await message.answer("✅ Jinsingiz aniqlandi endi yoshingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
            await Change_Age.get_for_age.set()
        else:
            await message.answer("✅Sizning jinsingiz erkak qilib belgilandi",reply_markup=main_menu)
    else:
        db.gender_update(message.from_user.id,'1')
        if age == 0:
            msg_get_age = await message.answer("✅ Jinsingiz aniqlandi endi yoshingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
            await Change_Age.get_for_age.set()
        else:
            await message.answer("✅Sizning jinsingiz erkak qilib belgilandi",reply_markup=main_menu)



@dp.message_handler(text='👩 Qiz bola')
async def set_gender(message:types.Message):
    if db.set_gender(message.from_user.id,'0'):
        db.add_balance(message.chat.id, config.DAILY_LIMIT)
        await asyncio.sleep(0.2)
        yosh = db.get_age(message.chat.id)
        if yosh == 0:
            msg_get_age = await message.answer("✅ Jinsingiz aniqlandi endi yoshingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
            await Change_Age.get_for_age.set()
        else:
            await message.answer("✅Sizning jinsingiz erkak qilib belgilandi",reply_markup=main_menu)
    else:
        db.gender_update(message.from_user.id,'0')
        if yosh == 0:
            msg_get_age = await message.answer("✅ Jinsingiz aniqlandi endi yoshingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
            await Change_Age.get_for_age.set()
        else:
            await message.answer("✅Sizning jinsingiz erkak qilib belgilandi",reply_markup=main_menu)


       
@dp.message_handler(state=Change_Age.get_for_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if 10 <= age <= 60:
            db.update_age(message.chat.id, age)
            await bot.delete_message(message.chat.id, message.message_id)
            await message.answer("✅Yoshingiz muvaffaqiyatli yangilandi!", reply_markup=main_menu)
            await state.finish()
        else:
            raise ValueError("Yosh 10 dan katta va 60 dan kichik bo'lishi kerak")
 
            await bot.delete_message(message.chat.id, message.message_id)
    except ValueError as e:
      
        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer(f"⚠️ Xatolik: Yosh notugri kiritildi yoki tugri yosh kiritilmadi! Min: 10, Max: 60")
        #await state.finish()
    finally:
        await state.finish()

