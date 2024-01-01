from loader import dp, bot, db
from aiogram import types
from aiogram.types import ParseMode, BotCommand






aloqa = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text='♻️ Bog’lanish',url='https://t.me/LazizbekDev')
        ]
    ]
)

@dp.message_handler(commands=['dev'])
async def stats_cmd(message: types.Message):
    chat_id = message.from_user.id
    photo_path = './assets/photos/dev.png'
    xabar = "*Bot dasturchisi*\: [LazizbekDev](https://t.me/LazizbekDev)\n\n*Ish vaqti\: 07:00 dan 01:00 gacha*\n\n*Telegramda Turli Xil Botlar Yaratish Xizmati *\!"
    await bot.send_photo(
    chat_id=message.chat.id,
    photo=types.InputFile(photo_path),
    caption=xabar,
    parse_mode=types.ParseMode.MARKDOWN_V2,
    reply_markup=aloqa
    )
    

