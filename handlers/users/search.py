from loader import dp, db, bot
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, Message
from keyboards.default import stop_menu, main_menu, stop_chat_menu,search_menu
from aiogram.dispatcher.filters import Command
from keyboards.inline import static
from data import config
import sqlite3
from keyboards.default import check_gender_menu






class ChangeAge(StatesGroup):
    waiting_for_age = State()



@dp.callback_query_handler(lambda c: c.data == 'change_age')
async def change_age_callback(query: CallbackQuery):
    global msg_edited
    msg_edited = await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="🔞 Iltimos yoshingizni kiriting...")
    await ChangeAge.waiting_for_age.set()



@dp.message_handler(state=ChangeAge.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if 10 <= age <= 60:
            db.update_age(message.chat.id, age)
            await msg_edited.delete()
            await bot.delete_message(message.chat.id, message.message_id)
            await message.answer("✅Yoshingiz muvaffaqiyatli yangilandi!")
            await state.finish()
        else:
            raise ValueError("Yosh 10 dan katta va 60 dan kichik bo'lishi kerak")
            await msg_edited.delete()
            await bot.delete_message(message.chat.id, message.message_id)
    except ValueError as e:
        await msg_edited.delete()
        await bot.delete_message(message.chat.id, message.message_id)
        await message.answer(f"⚠️ Xatolik: Yosh notugri kiritildi yoki tugri yosh kiritilmadi! Min: 10, Max: 60")
        #await state.finish()
    finally:
        await state.finish()





@dp.message_handler(commands=['yosh'])
async def set_age(message: types.Message):
    try:
        age = int(message.get_args())
        chat_id = message.chat.id
        db.update_age(message.chat.id, age)

        await message.reply(f"Yoshingiz {age} ga yangilandi!", parse_mode=ParseMode.MARKDOWN)

    except (ValueError, TypeError):
        await message.reply("Noto'g'ri format! Buyruqni shunday ishlating: `/yosh {yosh}`", parse_mode=ParseMode.MARKDOWN)






@dp.message_handler(text="❌Chatni To'xtatish")
async def stop(message: types.Message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info == None or False:
        await bot.send_message(message.chat.id, "❌Siz hali chatni boshlamagansiz", reply_markup=main_menu)
    else:
        db.delate_chats(chat_info[0])
        await bot.send_message(chat_info[1], "❌Suxbatdoshingiz chatni to'xtatdi", reply_markup=main_menu)
        await bot.send_message(message.chat.id, "❌Siz chatni to'xtatdingiz", reply_markup=main_menu)
    


def inline():
        user = "https://t.me/LazizbekDev"
        buttonurl = types.InlineKeyboardButton("💸 Hisobni toldirish", url=user)
        change_gen = types.InlineKeyboardButton("👤 Jinsni uzgartirish", callback_data="change_gen")
        change_age = types.InlineKeyboardButton("🔞 Yoshni uzgartirish", callback_data="change_age")
        inline = types.InlineKeyboardMarkup()
        inline.add(buttonurl)
        inline.add(change_gen)
        inline.add(change_age)
        return inline



@dp.callback_query_handler(text='change_gen')
async def change_gen(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)
    await bot.send_message(call.message.chat.id, "👇 Pastdagi tugamalar orqali jinsingizni tanlang!", reply_markup=check_gender_menu)



@dp.message_handler(content_types='text')
async def full_handler(message: types.Message):
    if message.text == "🔍Suxbatdosh Izlash":
        await message.answer("Kim bilan suxbat qurmoqchisiz", reply_markup=search_menu)
    elif message.text == "👥Jinsni o'zgartirish":
        await message.answer('👥Jinsingizni Ozgaritishingiz Mumkin', reply_markup=check_gender_menu)
    elif message.text == "❌Qidiruvni To'xtatish":
        db.delete_queue(message.chat.id)
        await bot.send_message(message.chat.id, "❌Qidiruv To'xtatildi\n📄Siz bosh Menuga qaytdingiz", reply_markup=main_menu)
    elif message.text == '📚Bot Haqida':
        activusers = db.users_count(1)
        await bot.send_message(message.from_user.id, f"👋 Assalomu Alaykum botimizga xush kelibsiz. ✅\n\n🔥 Ushbu bot orqali siz anonim suhbat qura olasiz... 😊\n‼️Diqqat har bir suhbat narxi 1 sum\n📃 Sizga kuniga {config.DAILY_LIMIT} ta tekin suhbat qilish imkoniyati beriladi\nAgar kunlik tekin suhbat tugab qolsa admin orqali qushimcha limit olishingiz mumkin! ⚠️Xizmat pullik\n\n👮‍♂️ Admin: {config.ADMIN}\n\n👁‍🗨Hozircha Men orqali {db.select_users_count()} ta odam bilan gaplasha olasiz\n\n♾Qani endi suxbatni boshlang", reply_markup=static)
    elif message.text == '🔝Bosh Menuga Qaytish':
        await bot.send_message(message.from_user.id, "Bosh Menuga qaytdingiz", reply_markup=main_menu)
    elif message.text == '👤 Profil':
        gender = db.get_gender(message.chat.id)
        if gender == '1':
            jins = "O'g'il bola"
        elif gender == '0':
            jins = "Qiz bola"
        else:
            jins = "nomalum"
        
        age = db.get_age(message.chat.id)
        balance = db.get_balance(message.chat.id)
        await message.reply(f'💰 Kabinet ga xush kelibsiz!\n\n🔞 Yoshingiz: {age}\n👤 Jinsingiz: {jins}\n💸 Balance: {balance}\n🆔ID: {message.chat.id}', reply_markup=inline())



    elif message.text == '/accaunt':
        gender = db.get_gender(message.chat.id)
        if gender == '1':
            jins = "O'g'il bola"
        elif gender == '0':
            jins = "Qiz bola"
        else:
            jins = "nomalum"
        
        age = db.get_age(message.chat.id)
        balance = db.get_balance(message.chat.id)
        await message.reply(f'💰 Kabinet ga xush kelibsiz!\n\n🔞 Yoshingiz: {age}\n👤 Jinsingiz: {jins}\n💸 Balance: {balance}\n🆔ID: {message.chat.id}', reply_markup=inline())


    
    #Random user qidirish funksiyasi
    elif message.text =="🫂 Suxbatdosh izlash":
        user_info = db.get_chats()
        chat_two = user_info[0]
            # print(chat_two)

        if db.create_chat(message.chat.id, chat_two) == False:
            db.add_queue(message.chat.id,db.get_gender(message.chat.id))
            await bot.send_message(message.chat.id, "💬Suxabatdosh Qidirilmoqda...", reply_markup=stop_menu)
        else:
            msg = "🎉 Suxbatdosh topildi!! \n💸 Hisobingizdan 0 yechildi!\nSuxbat-ni toxtatish uchun pastdagi tugmani bosing❗"
            await bot.send_message(message.chat.id, msg, reply_markup=stop_chat_menu)
            await bot.send_message(chat_two, msg, reply_markup=stop_chat_menu)
        
    #Erkaklar qidiruvi
    
    elif message.text == "🤴 O'g'il bola":
        success = db.rm_balance(message.chat.id, 1)
        if success:
            user_info = db.get_gender_chat('1')
            chat_two = user_info[0]
            #print(chat_two)
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id,db.get_gender(message.chat.id))
                await bot.send_message(message.chat.id, "💬Suxabatdosh Qidirilmoqda...", reply_markup=stop_menu)
            else:
                gender_two = db.get_gender(chat_two)
                gender = db.get_gender(message.chat.id)
                
                if gender_two == "1":
                    gen_two = "🤴 O'g'il bola"
                else:
                    gen_two = "👸 Qiz bola"
                
                if gender == "1":
                    gen = "🤴 O'g'il bola"
                else:
                    gen = "👸 Qiz bola"
                
                await bot.send_message(message.chat.id, f"🎉 Suxbatdosh topildi!! \n\n👤 Jinsi: {gen_two}\n🔞Yoshi: {db.get_age(chat_two)}\n\n💸 Hisobingizdan 1 yechildi!\nSuxbat-ni toxtatish uchun pastdagi tugmani bosing❗", reply_markup=stop_chat_menu)
                await bot.send_message(chat_two, f"🎉 Suxbatdosh topildi!! \n\n👤 Jinsi: {gen}\n🔞Yoshi: {db.get_age(message.chat.id)}\n\n💸 Hisobingizdan 1 yechildi!\nSuxbat-ni toxtatish uchun pastdagi tugmani bosing❗", reply_markup=stop_chat_menu)
        else:
            await message.answer(f"⚠️ Hisobingizda mablag yetarli emas! Kunlik limit ni oshirish uchun adminga mutojaat qiling!\n👮‍♂️Admin: {config.ADMIN}")

            
    elif message.text == "👸 Qiz bola":
        success = db.rm_balance(message.chat.id, 1)
        if success:
            user_info = db.get_gender_chat('0')
            chat_two = user_info[0]
           # print(chat_two)

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id,db.get_gender(message.chat.id))
                await bot.send_message(message.chat.id, "💬Suxabatdosh Qidirilmoqda...", reply_markup=stop_menu)
            else:
                gender_two = db.get_gender(chat_two)
                gender = db.get_gender(message.chat.id)
                
                if gender_two == "1":
                    gen_two = "🤴 O'g'il bola"
                else:
                    gen_two = "👸 Qiz bola"
                
                if gender == "1":
                    gen = "🤴 O'g'il bola"
                else:
                    gen = "👸 Qiz bola"
                
                await bot.send_message(message.chat.id, f"🎉 Suxbatdosh topildi!! \n\n👤 Jinsi: {gen_two}\n🔞Yoshi: {db.get_age(chat_two)}\n\n💸 Hisobingizdan 1 yechildi!\nSuxbat-ni toxtatish uchun pastdagi tugmani bosing❗", reply_markup=stop_chat_menu)
                await bot.send_message(chat_two, f"🎉 Suxbatdosh topildi!! \n\n👤 Jinsi: {gen}\n🔞Yoshi: {db.get_age(message.chat.id)}\n\n💸 Hisobingizdan 1 yechildi!\nSuxbat-ni toxtatish uchun pastdagi tugmani bosing❗", reply_markup=stop_chat_menu)
        else:
            await message.answer(f"⚠️ Hisobingizda mablag yetarli emas! Kunlik limit ni oshirish uchun adminga mutojaat qiling!\n👮‍♂️Admin: {config.ADMIN}")
            
            
    
    else:
        if db.get_active_chat(message.chat.id):
            chat_info = db.get_active_chat(message.chat.id)
            await bot.send_message(chat_info[1],message.text)
        else:
            await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")
            
@dp.message_handler(content_types='sticker')
async def send_sticers(message:types.Message):
    if db.get_active_chat(message.chat.id):
            chat_info = db.get_active_chat(message.chat.id)
            await bot.send_sticker(chat_info[1],message.sticker.file_id)
    else:
        await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")
    
@dp.message_handler(content_types='voice')
async def send_sticers(message:types.Message):
    if db.get_active_chat(message.chat.id):
            chat_info = db.get_active_chat(message.chat.id)
            await bot.send_voice(chat_info[1],message.voice.file_id)
    else:
        await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")

@dp.message_handler(content_types='document')
async def send_sticers(message:types.Message):
    if db.get_active_chat(message.chat.id):
            chat_info = db.get_active_chat(message.chat.id)
            await bot.send_document(chat_info[1],message.document.file_id)
    else:
        await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")
        
# @dp.message_handler(content_types='video')
# async def send_sticers(message:types.Message):
#     if db.get_active_chat(message.chat.id):
#             chat_info = db.get_active_chat(message.chat.id)
#             await bot.send_video(chat_info[1],message.document.file_id)
#     else:
#         await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")
        
@dp.message_handler(content_types='photo')
async def send_photo(message: types.Message):
    if db.get_active_chat(message.chat.id):
            chat_info = db.get_active_chat(message.chat.id)
            await bot.send_photo(chat_info[1],photo=message.photo[-1].file_id)
    else:
        await bot.send_message(message.chat.id,"🚫Bunday Buyruq Mavjud Emas")


        
