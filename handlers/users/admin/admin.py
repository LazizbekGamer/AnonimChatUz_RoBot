from aiogram import types
from data.config import ADMINS
from keyboards.default.admin_panel import admin_menu
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.admin_panel import mailing_menu
from keyboards.default import main_menu
from aiogram.dispatcher import FSMContext
from states import bot_mailing
from states import bot_mailing_photo
from states.admin import set_balance, get_new_balance, rm_balance, get_rm_balance, get_balance
from loader import dp,db,bot



@dp.message_handler(Command(['admin', 'panel']))
async def welcome_admin(message: types.Message):
    for admin in ADMINS:
        if message.chat.id == admin:
            await bot.send_message(message.chat.id,"Assalomu aleykum admin",reply_markup=admin_menu)
        else:
            pass



@dp.message_handler(lambda message: message.text == '💰Pul-qoshish' and message.from_user.id in ADMINS)
async def admin_handler(message: types.Message, state: FSMContext):
    await message.answer("💰 Pul qushmoqchi bolgan foyfalanuvchi ChatID ni kiriting!")
    await state.set_state("set_balance")



@dp.message_handler(state="set_balance")
async def set_balance_handler(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)
    except ValueError:
        await message.answer("Chat ID xato kiritildi. Iltimos, qaytadan kiriting.")
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(f"{chat_id} foydalanuvchi uchun qanday mablag'ni qo'shmoqchisiz?")
    await state.set_state("get_new_balance")



@dp.message_handler(state="get_new_balance")
async def get_new_balance_handler(message: types.Message, state: FSMContext):
    try:
        balance = int(message.text)
    except ValueError:
        await message.answer("Xato mablag' kiritildi. Iltimos, qaytadan kiriting.")
        return

    
    data = await state.get_data()
    chat_id = data.get("chat_id")
    bal = data.get("balance")
    success_msg = f"🆕 Sizga admin tomonidan {balance}$ tulab berildi!"
    db.add_balance(chat_id, balance)
    await message.answer(f"{chat_id} foydalanuvchiga {balance}$ pul qo'shildi.")
    await bot.send_message(chat_id, success_msg)
    await state.finish()



@dp.message_handler(lambda message: message.text == '💰Pul-qoshish' and message.from_user.id in ADMINS)
async def admin_handler(message: types.Message, state: FSMContext):
    await message.answer("💰 Pul qushmoqchi bolgan foydalanuvchi ChatID ni kiriting!")
    await state.set_state("set_balance")



def userlist(self):
        admins_cid = db.select_all()
        inline_keyboard = []
        row = []
        for admin_id in admins_cid:
            tg_user = f"tg://user?id={admin_id}"
            inline_button = types.InlineKeyboardButton(f'{admin_id}', url=tg_user)
            row.append(inline_button)
            if len(row) == 2:
                inline_keyboard.append(row)
                row = []
                
        if row:
            inline_keyboard.append(row)
            
        btn = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return btn

@dp.message_handler(lambda message: message.text == '👤 Userlar Ruyhati' and message.from_user.id in ADMINS)
async def admin_user_handler(message: types.Message, state: FSMContext):
    await message.answer("👇 Botdagi foydalanuvchilar ruyhati", reply_markup=userlist(dp))



@dp.message_handler(state="set_balance")
async def set_balance_handler(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)
    except ValueError:
        await message.answer("Chat ID xato kiritildi. Iltimos, qaytadan kiriting.")
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(f"{chat_id} foydalanuvchi uchun qancha mablag'ni qo'shmoqchisiz?")
    await state.set_state("get_new_balance")



# pul ayirish
@dp.message_handler(lambda message: message.text == '💰Pul-ayirish' and message.from_user.id in ADMINS)
async def admin_handler(message: types.Message, state: FSMContext):
    await message.answer("💰 Pul ayirmoqchi bolgan foydalanuvchi ChatID ni kiriting!")
    await state.set_state("rm_balance")



@dp.message_handler(state="rm_balance")
async def rm_balance_handler(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)
    except ValueError:
        await message.answer("Chat ID xato kiritildi. Iltimos, qaytadan kiriting.")
        return

    await state.update_data(chat_id=chat_id)
    await message.answer(f"{chat_id} foydalanuvchi uchun qancha mablag'ni ayirmoqchisiz?")
    await state.set_state("get_rm_balance")



@dp.message_handler(state="get_rm_balance")
async def get_rm_balance_handler(message: types.Message, state: FSMContext):
    try:
        balance = int(message.text)
    except ValueError:
        await message.answer("Xato mablag' kiritildi. Iltimos, qaytadan kiriting.")
        return

    
    data = await state.get_data()
    chat_id = data.get("chat_id")
    bal = data.get("amount")
    success_msg = f"🆕 Sizdan admin tomonidan {balance}$ ayirildi!"
    success = db.rm_balance(chat_id, balance)
    if success:
        await message.answer(f"{chat_id} foydalanuvchidan {balance}$ pul ayiril.")
        await bot.send_message(chat_id, success_msg)
        await state.finish()
    else:
        await message.answer(f"{chat_id} foydalanuvchidan {balance}$ pul ayirilmadi. Pul yetarli emas")
        await state.finish()



# get balance
@dp.message_handler(lambda message: message.text == '💰Pul-aniqlash' and message.from_user.id in ADMINS)
async def admin_balance_handler(message: types.Message, state: FSMContext):
    await message.answer("💵 Balance ni aniqlamoqchi bo'lgan foydalanuvchi ChatID ni kiriting...")

    await state.set_state("get_balance")



@dp.message_handler(state="get_balance")
async def get_balance_handler(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)
    except ValueError:
        await message.answer("Chat ID xato kiritildi. Iltimos, qaytadan kiriting.")
        return

    await state.update_data(chat_id=chat_id)

    data = await state.get_data()
    chat_id = data.get("chat_id")
    balance = db.get_balance(chat_id)

    await message.answer(f"👤 {chat_id} foydalanuvchining balance si {balance}$")
    await state.finish()



@dp.message_handler(text='📤Xabar')
async def start_mailing(message:types.Message):
    await bot.send_message(message.chat.id,"Xabar Yuborish Turini Tanlang",reply_markup=mailing_menu)



#Matnli xabar yuborish funksiyasi
@dp.message_handler(text='⌨️Matnli Xabar Yuborish')
async def set_text(message:types.Message,state:FSMContext):
    for admin in ADMINS:
        if message.chat.id == admin:
            await message.answer("Matn kiriting")
            await bot_mailing.text.set()
        else:
            await state.finish()



@dp.message_handler(state=bot_mailing.text)
async def send_text(message:types.Message,state:FSMContext):
    for admin in ADMINS:
        if message.chat.id == admin:
            answer = message.text
            await state.update_data(text=answer)

            data = await state.get_data()

            text = data.get('text')
            #Idlarni bazadan oladi va Matn yuboradi
            for admin in ADMINS:
                if message.chat.id == admin:
                    users = db.get_users()
                    for i in users:
                            try:
                                await bot.send_message(i[0], text)
                                if int(i[1]) != 1:
                                    db.set_active(i[0],1)
                            except:
                                    db.set_active(i[0],0)
    await state.finish()



#Rasm va Xabar-li jonatmalar funksiyasi
@dp.message_handler(text='🌠Rasmli Xabar Yuborish')
async def set_photo(message: types.Message,state:FSMContext):
    for admin in ADMINS:
        if message.chat.id == admin:
            await message.answer("Matn kiriting")
            await bot_mailing_photo.photo_text.set()
        else:
            await state.finish()



@dp.message_handler(state=bot_mailing_photo.photo_text)
async def sendphoto_text(message:types.Message,state:FSMContext):
    answer_text = message.text
    await state.update_data(photo_text=answer_text)
    await bot.send_message(message.chat.id,"Xabar uchun rasm yuboring")
    await bot_mailing_photo.photo.set()



@dp.message_handler(state=bot_mailing_photo.photo,content_types=types.ContentType.PHOTO)
async def send_photo(message:types.Message,state:FSMContext):
    answer_photo = message.photo[-1].file_id
    await state.update_data(photo=answer_photo)
    data = await state.get_data()
    photo_text = data.get('photo_text')
    photo = data.get('photo')
    #Idlarni bazadan oladi va Matn yuboradi
    for admin in ADMINS:
        if message.chat.id == admin:
            users = db.get_users()
            for i in users:
                    try:
                        await bot.send_photo(i[0],photo=photo,caption=photo_text)
                        if int(i[1]) != 1:
                            db.set_active(i[0],1)
                    except:
                            db.set_active(i[0],0)
        
    await state.finish()



@dp.message_handler(text='📊Statistika')
async def static(message:types.Message):
    for admin in ADMINS:
        if message.chat.id == admin:
           count = db.select_users_count()
           await bot.send_message(message.chat.id,f"Bot Statistikasi:\n\n Userlar soni: {count} ta") 