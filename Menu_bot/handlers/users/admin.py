import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.boshmenu_va_jonatish_button import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from states.ishga_qabul import *
from loader import dp, bot, base


@dp.message_handler(commands='admin', chat_id = [i for  i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
   await message.answer(text='Yangi taom qoshish uchun', reply_markup=homeIsAdminPanel)


@dp.message_handler(text="Qo'shish", chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    keys = []
    keys.append([InlineKeyboardButton(text=f"Taom", callback_data=f"fastFoodAdmin"),
                 InlineKeyboardButton(text="Ichimliklar", callback_data="ichimliklarAdmin")])
    taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
    await message.answer(text="Taom yoki Ichimlik qo'shish uchun tanlang", reply_markup=taom_menu)

@dp.message_handler(text="O'chirish", chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    keys = []
    keys.append([InlineKeyboardButton(text=f"Taom", callback_data=f"fastfoodDel"),
             InlineKeyboardButton(text="Ichimliklar", callback_data="ichimlikDel")])
    taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
    await message.answer(text="Taom yoki Ichimlik o'chirish uchun tanlang", reply_markup=taom_menu)

@dp.message_handler(text="Bot a'zolari", chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    bot_azo = base.usersCount()
    await message.answer(text=f"Bot A'zolari soni\n {bot_azo}")


@dp.message_handler(state=Foods.foodName_state)
async def bot_echo(message: types.Message, state: FSMContext):
    food = message.text
    await state.update_data({"name": food})
    await message.answer(text="Narxini kiriting")
    await Foods.price_state.set()

@dp.message_handler(state=Foods.price_state)
async def bot_echo(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({"price": price})
    await message.answer(text="Gcatalogini kiriting\nEslatma:  fastfood")
    await Foods.gcatalog_state.set()

@dp.message_handler(state=Foods.gcatalog_state)
async def bot_echo(message: types.Message, state: FSMContext):
    gcatalog = message.text
    await state.update_data({"catalog": gcatalog})
    await message.answer(text="Statusni kiriting")
    await Foods.status_state.set()


@dp.message_handler(state=Foods.status_state)
async def bot_echo(message: types.Message, state: FSMContext):
    status = message.text
    await state.update_data({"status": status})
    await message.answer(text="✅ Kiritgan ma'lumotlaringizni tasdiqlaysizmi")

    inform = await state.get_data()
    name = inform.get('name')
    price = inform.get('price')
    catalog = inform.get('catalog')
    status = inform.get('status')

    text = f"✅Taom:  {name}\n" \
           f"✅Narxi:  {price}\n" \
           f"✅Catalog:  {catalog}\n" \
           f"✅Status:  {status}" \

    await message.answer(text=text, reply_markup=ha_yoq)
    await Foods.tasdiqlash_state.set()

@dp.message_handler(state=Foods.tasdiqlash_state,text="Ha")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    inform = await state.get_data()
    name = inform.get('name')
    price = inform.get('price')
    catalog = inform.get('catalog')
    status = inform.get('status')

    base.foodAdd(name=name, price=price, gcatalog=catalog, status=status)

    text = f"✅Taom:  {name}\n" \
           f"✅Narxi:  {price}\n" \
           f"✅Catalog:  {catalog}\n" \
           f"✅Status:  {status}" \

    await bot.send_message(chat_id="603002344", text=text)
    await bot.send_message(chat_id=user_id, text="🛫 Malumotingiz Bazaga qoshildi Sorov uchun raxmat", reply_markup=homeIsAdminPanel)
    await state.finish()

@dp.message_handler(state=Foods.tasdiqlash_state, text="Yo'q")
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(text="Bekor qilindi",reply_markup=homeIsAdminPanel)
    await state.finish()


########################## for drinks ########################################################################################

@dp.message_handler(state=Drink.drinkName_state)
async def bot_echo(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name": name})
    await message.answer(text="ichimlikingizni bir martalik yoki kop martalik litri boyicha kiriting\n"
                              , reply_markup=litr)
    await Drink.litr_state.set()

#################################### BIR MARTALIK ZAKAZ BOYIVHA ########################################################

@dp.message_handler(state=Drink.litr_state,text="Bir litrlik")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="Ichimlikni bir martalik litri bo'yicha narxini kiriting:")
    await Drink.price_1_state.set()

@dp.message_handler(state=Drink.price_1_state)
async def bot_echo(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({"price1": price})
    await message.answer(text="Gcatalogni kiritng\nEslatma: ichimlik:")
    await Drink.gcatalog_state.set()


####################### KOP MARTALIK ZAKAZ BOYICHA #####################################################################

@dp.message_handler(state=Drink.litr_state,text="Ko'p litrlik")
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id, text="1.5l Ichimlikni litri bo'yicha narxini kiriting:")
    await Drink.price_15l_state.set()

@dp.message_handler(state=Drink.price_15l_state)
async def bot_echo(message: types.Message, state: FSMContext):
    price = message.text
    await state.update_data({"price15l": price})
    await message.answer(text="1l Ichimlikni litri bo'yicha narxini kiriting:")
    await Drink.price_1l_state.set()

@dp.message_handler(state=Drink.price_1l_state)
async def bot_echo(message: types.Message, state: FSMContext):
    price1 = message.text
    await state.update_data({"price1l": price1})
    await message.answer(text="0.5l Ichimlikni litri bo'yicha narxini kiriting:")
    await Drink.price_05l_state.set()

@dp.message_handler(state=Drink.price_05l_state)
async def bot_echo(message: types.Message, state: FSMContext):
    price2 = message.text
    await state.update_data({"price05l": price2})
    await message.answer(text="Gcatalogni kiritng\nEslatma: ichimlik")
    await Drink.gcatalog_state.set()


@dp.message_handler(state=Drink.gcatalog_state)
async def bot_echo(message: types.Message, state: FSMContext):
    gcatalog = message.text
    await state.update_data({"gcatalog": gcatalog})
    await message.answer(text="Statusni kiriting\nEslatma: active")
    await Drink.status_state.set()

@dp.message_handler(state=Drink.status_state)
async def bot_echo(message: types.Message, state: FSMContext):
    status = message.text
    await state.update_data({"status": status})
    await message.answer(text="✅ Kiritgan ma'lumotlaringizni tasdiqlaysizmi")
    user_id = message.from_user.id
    inform = await state.get_data()

    name = inform.get('name')
    price1 = inform.get('price1')
    price15l = inform.get('price15l')
    price1l = inform.get('price1l')
    price05l = inform.get('price05l')
    gcatalog = inform.get('gcatalog')
    status = inform.get('status')

    if price15l and price1l and price05l:
        text = f"✅Taom:  {name}\n" \
               f"✅Narxi 1.5L:  {price15l}\n" \
               f"✅Narxi 1L:  {price1l}\n" \
               f"✅Narxi 0.5L:  {price05l}\n" \
               f"✅Gcatalog:  {gcatalog}\n" \
               f"✅Status:  {status}"
        await message.answer(text=text, reply_markup=ha_yoq)
        await Drink.tasdiqlash_state.set()

    elif price1:
        text = f"✅Taom:  {name}\n" \
               f"✅Narxi 1L:  {price1}\n" \
               f"✅Gcatalog:  {gcatalog}\n" \
               f"✅Status:  {status}"
        await message.answer(text=text, reply_markup=ha_yoq)
        await Drink.tasdiqlash_state.set()

    else:
        await bot.send_message(chat_id=user_id, text="🛫 Malumotingizda Xatolik bor."
                                                     " Ichimlik litri boyicha narx qo'shilmadi", reply_markup=litr)

@dp.message_handler(state=Drink.tasdiqlash_state,text="Ha")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    inform = await state.get_data()
    name = inform.get('name')
    price1 = inform.get('price1')
    price15L = inform.get('price15l')
    price1L = inform.get('price1l')
    price05L = inform.get('price05l')
    gcatalog = inform.get('gcatalog')
    status = inform.get('status')

    if price15L and price1L and price05L:
        base.drinkAdd(name=name, price1=price15L, price2=price1L, price3=price05L, gcatalog=gcatalog, status=status)
        await bot.send_message(chat_id=user_id, text="🛫 Malumotingiz Bazaga qoshildi ichimlik ko'p martalik litr uchun",
                               reply_markup=homeIsAdminPanel)
        await state.finish()
    elif price1:
        base.drinkAdd(name=name, price2=price1, gcatalog=gcatalog, status=status)
        await bot.send_message(chat_id=user_id, text="🛫 Malumotingiz Bazaga qoshildi ichimlik bir martalik litr uchun",
                               reply_markup=homeIsAdminPanel)
        await state.finish()
    else:
        await bot.send_message(chat_id=user_id, text="🛫 Malumotingizda Xatolik bor."
                                                 " Ichimlik litri boyicha narx qo'shilmadi", reply_markup=litr)
    await state.finish()


@dp.message_handler(state=Drink.tasdiqlash_state, text="Yo'q")
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(text="Bekor qilindi",reply_markup=homeIsAdminPanel)
    await state.finish()

################################## for calculating all of price ########################################################

@dp.message_handler(commands='hisob', chat_id = [i for  i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    await message.answer(text="Sizga qaysi turdagi ✅Hisobot kerak", reply_markup=date)

@dp.message_handler(text='Hozirgi Kun', chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    vaqtDay = datetime.datetime.now().strftime("%d")
    weekDay = datetime.datetime.now().strftime("%A")
    if weekDay == "Monday":
        week = "Dushanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Tuesday":
        week = "Seshanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Wednesday":
        week = "Chorshanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Thursday":
        week = "Payshanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Friday":
        week = "Juma"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Saturday":
        week = "Shanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")
    elif weekDay == "Sunday":
        week = "Yakshanba"
        i = base.calculateArxivDay(day=vaqtDay)
        for hisob in i:
            await message.answer(text=f"{vaqtDay}-{week} kunining Umumiy hisobi 💵{hisob} So'm")


@dp.message_handler(text='Hozirgi Oy', chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    vaqtMonth = datetime.datetime.now().strftime("%m")
    month = datetime.datetime.now().strftime("%B")
    if month == "January ":
        month1 = "Yanvar"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "February":
        month1 = "Fevral"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "March":
        month1 = "Mart"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "April":
        month1 = "Aprel"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "May":
        month1 = "May"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "June":
        month1 = "Iyun"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "July":
        month1 = "Iyul"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "August":
        month1 = "Avgust"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "September":
        month1 = "Sentyabr"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "October":
        month1 = "Octyabr"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "November":
        month1 = "Noyabr"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")
    elif month == "December":
        month1 = "Dekabr"
        i = base.calculateArxivMonth(month=vaqtMonth)
        for hisob in i:
            await message.answer(text=f"{month1} oyining Umumiy hisobi 💵{hisob} So'm")


@dp.message_handler(text='Eski hisobot', chat_id=[i for i in [603002344, 594966461]])
async def bot_echo(message: types.Message):
    await message.answer("Hisobotni Kuni yoki Oyini tanlang", reply_markup=date1)
    await Hisob.tanlash_state.set()

@dp.message_handler(state=Hisob.tanlash_state, text="Kun")
async def bot_echo(message: types.Message):
    await message.answer(text="Hisobni kuni bo'yicha kiriting\nMisol uchun: 1 dan 31 Kungacha")
    await Hisob.kun_state.set()
@dp.message_handler(state=Hisob.kun_state)
async def bot_echo(message: types.Message, state: FSMContext):
    kun = message.text
    i = base.calculateArxivDay(day=kun)
    for hisob in i:
        await message.answer(text=f"{kun} kunining Umumiy hisobi 💵{hisob} So'm")
    await state.finish()


@dp.message_handler(state=Hisob.tanlash_state, text="Oy")
async def bot_echo(message: types.Message):
    await message.answer(text="Hisobni Oyi bo'yicha kiriting\nMisol uchun: 1 dan 12 Oygacha")
    await Hisob.oy_state.set()
@dp.message_handler(state=Hisob.oy_state)
async def bot_echo(message: types.Message, state: FSMContext):
    oy = message.text
    i = base.calculateArxivMonth(month=oy)
    for hisob in i:
        await message.answer(text=f"{oy} Oyining Umumiy hisobi 💵{hisob} So'm")
    await state.finish()