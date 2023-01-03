from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.boshmenu_va_jonatish_button import buyurtma_tugmasi
from loader import dp, base


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    qoshimcha = "Appetit_FastFood yetkazib berish xizmatiga xush kelibsiz Locatsiyani jo'nating"
    await message.answer(f"Assalomu alaykum! {message.from_user.full_name}!\n {qoshimcha}\n ",
                         reply_markup=buyurtma_tugmasi)

    ism = message.from_user.first_name
    fam = message.from_user.last_name
    user = message.from_user.username
    idd = message.from_user.id
    try:
        base.user_qoshish(ism=ism, tg_id=idd, fam=fam, username=user)
    except Exception as xatolik:
        print(xatolik)
