from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.boshmenu_va_jonatish_button import buyurtma_tugmasi, ha_yoq
from states.ishga_qabul import Malumot
from loader import dp, bot


@dp.message_handler(text="๐ Jamoamizga qo'shiling")
async def bot_echo(message: types.Message):
    await message.answer(text="Ismingizni kiriting ๐")
    await Malumot.ism_state.set()

@dp.message_handler(state=Malumot.ism_state)
async def bot_echo(message: types.Message, state: FSMContext):
    ism = message.text
    await state.update_data({"name": ism})
    await message.answer(text="๐ฐ Yoshingizni kiriting\nMisol uchun: 22")
    await Malumot.yosh_state.set()

@dp.message_handler(state=Malumot.yosh_state)
async def bot_echo(message: types.Message, state: FSMContext):
    yosh = message.text
    await state.update_data({"age": yosh})
    await message.answer(text="โ Telefon raqamingizni kiriting\nMisol uchun: +998901234567")
    await Malumot.tel_state.set()

@dp.message_handler(state=Malumot.tel_state)
async def bot_echo(message: types.Message, state: FSMContext):
    ish_turi = message.text
    await state.update_data({"work": ish_turi})
    await message.answer(text="๐  Qanday ish turi bilan ishga kirmoqchisiz\nMisol uchun: Oshpazlik ")
    await Malumot.ish_state.set()

@dp.message_handler(state=Malumot.ish_state)
async def bot_echo(message: types.Message, state: FSMContext):
    tel = message.text
    await state.update_data({"number": tel})
    await message.answer(text="โ Kiritgan ma'lumotlaringizni tasdiqlaysizmi")

    inform = await state.get_data()
    ism = inform.get('name')
    yosh = inform.get('age')
    tell = inform.get('number')
    ish_turi = inform.get('work')

    text = f"โIsm:  {ism}\n" \
           f"โYosh:  {yosh}\n" \
           f"โTel raqam:  {tell}\n" \
           f"โIsh_turi:  {ish_turi}" \

    await message.answer(text=text, reply_markup=ha_yoq)
    await Malumot.tasdiqlash.set()

@dp.message_handler(state=Malumot.tasdiqlash,text="Ha")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    inform = await state.get_data()
    ism = inform.get('name')
    yosh = inform.get('age')
    tell = inform.get('number')
    ish_turi = inform.get('work')

    text = f"โIsm:  {ism}\n" \
           f"โYosh:  {yosh}\n" \
           f"โTel raqam:  {tell}\n" \
           f"โIsh_turi:  {ish_turi}" \


    await bot.send_message(chat_id="603002344", text=text)
    await bot.send_message(chat_id=user_id, text="๐ซ Malumotingiz adminga yuborildi.\n โ๏ธTez orada siz bilan bog'lanamiz\n"
                                            "Sorov uchun raxmat", reply_markup=buyurtma_tugmasi)
    await state.finish()

@dp.message_handler(state=Malumot.tasdiqlash, text="Yo'q")
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(text="Bekor qilindi",reply_markup=buyurtma_tugmasi)
    await state.finish()
