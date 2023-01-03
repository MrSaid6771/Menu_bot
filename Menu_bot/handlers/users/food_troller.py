from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery

from keyboards.default.boshmenu_va_jonatish_button import forKarzinka
from loader import dp, base, bot
from states.ishga_qabul import Foods, Drink


@dp.message_handler(text='🍔 FastFood')
async def bot_echo(message: types.Message):
    taomlar = base.select_all_foods()
    keys = []
    for taom in (taomlar):
        id = taom[0]
        nomi = taom[1]
        price = taom[2]
        keys.append([InlineKeyboardButton(text=f"{nomi} - {price} 💸", callback_data=f"foods {id}")])
    taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
    await message.answer(text="*Quyidagi taomlani tanlang* 👇", parse_mode="markdown", reply_markup=taom_menu)


@dp.message_handler(text='🍹 Ichimliklar')
async def bot_echo(message: types.Message):
    drink = base.select_all_drinks()
    keys = []
    for drinks in drink:
        id = drinks[0]
        nomi = drinks[1]
        keys.append([InlineKeyboardButton(text=f"🍾 {nomi} ", callback_data=f"ichimliklar {id}")])
    taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
    await message.answer(text="*Ichimlikni tanlang* 👇", parse_mode="markdown", reply_markup=taom_menu)


@dp.message_handler(text="Savatcha🛒")
async def foodGet(message: types.Message):
    user_id = message.from_user.id
    savat = base.selectKarzinka(user_id=user_id, status="active")
    summa = 0
    keys = []
    for savatcha in savat:
        if savatcha[7] == 'fastfood':
            id = savatcha[0]
            nomi = savatcha[2]
            count = savatcha[3]
            if savatcha[4]:
                summa += int(savatcha[4])
            keys.append([InlineKeyboardButton(text=f"{nomi} - {count} ta", callback_data=f"foods {id}"),
                     InlineKeyboardButton(text=f"O'chirish", callback_data=f"delete {id}")])
        elif savatcha[7] == 'drink':
            id = savatcha[0]
            nomi = savatcha[2]
            count = savatcha[3]
            types = savatcha[6]
            if savatcha[4]:
                summa += int(savatcha[4])
            keys.append([InlineKeyboardButton(text=f"{nomi} {types}  - {count} ta", callback_data=f"foods {id}"),
                         InlineKeyboardButton(text=f"O'chirish", callback_data=f"delete {id}")])
    if len(savat) == 0:
        taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
        await bot.send_message(chat_id=user_id, text=f"🛒Savatchada hech narsa yo'q", reply_markup=taom_menu)
    else:
        taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
        await bot.send_message(chat_id=user_id, text=f"🛒Sizning buyurtmalaringiz\nSumma : {summa}-so'm", reply_markup=taom_menu)
    await message.answer(text="Taom uchun \"Commend 📝\" yozishni ham unutmang ", reply_markup=forKarzinka)



@dp.callback_query_handler()
async def forDeletes(message: CallbackQuery):
    data = message.data
    user_id = message.from_user.id

    if not data.find('count'):
        dataCall = data.split(" ")
        foodId = dataCall[2]
        count = dataCall[3]
        food = base.selectFood(id=foodId)
        foodName = food[1]
        foodPrice = food[2] * int(count)
        base.korzinkaAddFood(user_id=user_id, food_name=foodName, count=count, sum=foodPrice,
                             status='active', catalog= 'fastfood', )
        await bot.send_message(chat_id=user_id, text=f"Taom qoshildi👇  \nTaom: {foodName} 🍔\n"
                                                     f"Soni: {count} 🔄\nXisob: {foodPrice} 💵\n \n"
                                                     f"Agar sizga yana boshqa taom kerak bolsa tanlashingiz mumkin"
                                                     f" yoki 'Savatcha🛒' bo'limi orqali buyurtma bering ")

    if not data.find('sanash'):
        dataCall = data.split(" ")
        drinkId = dataCall[3]
        drinkTypes = dataCall[4]
        count = dataCall[5]
        drink = base.selectDrink(id=drinkId)
        drinkName = drink[1]
        if dataCall[4] == '1.5L':
            if drink[4] != None:
                drinkPrice = drink[4] * int(count)
                base.korzinkaAddDrink(user_id=user_id, food_name=drinkName, count=count, sum=drinkPrice,
                                      status='active', catalog='drink', types=drinkTypes)
                await bot.send_message(chat_id=user_id,
                                       text=f"Ichimlik qoshildi👇  \n\nIchimlik: {drinkName}  {drinkTypes}🍾\n"
                                            f"Soni: {count} 🔄\nXisob: {drinkPrice} 💵\n \n"
                                            f"Agar sizga yana boshqa taom kerak bolsa tanlashingiz mumkin"
                                            f" yoki 'Savatcha🛒' bo'limi orqali buyurtma bering ")
            else:
                await bot.send_message(chat_id=user_id,
                                       text=f"Kechirasiz 🍾{drinkName} ning 1.5l turdagi ichimlik yo'q" )
        elif dataCall[4] == '1L':
            if drink[5] != None:
                drinkPrice = drink[5] * int(count)
                base.korzinkaAddDrink(user_id=user_id, food_name=drinkName, count=count, sum=drinkPrice,
                                      status='active', catalog='drink', types=drinkTypes)
                await bot.send_message(chat_id=user_id,
                                       text=f"Ichimlik qoshildi👇  \n\nIchimlik: {drinkName}  {drinkTypes}🍾\n"
                                            f"Soni: {count} 🔄\nXisob: {drinkPrice} 💵\n \n"
                                            f"Agar sizga yana boshqa taom kerak bolsa tanlashingiz mumkin"
                                            f" yoki 'Savatcha🛒' bo'limi orqali buyurtma bering ")
            else:
                await bot.send_message(chat_id=user_id,
                                       text=f"Kechirasiz 🍾{drinkName} ning 1l turdagi ichimlik yo'q" )

        elif dataCall[4] == '0.5L':
            if drink[6] != None:
                drinkPrice = drink[6] * int(count)
                base.korzinkaAddDrink(user_id=user_id, food_name=drinkName, count=count, sum=drinkPrice,
                                      status='active', catalog='drink', types=drinkTypes)
                await bot.send_message(chat_id=user_id,
                                       text=f"Ichimlik qoshildi👇  \n\nIchimlik: {drinkName}  {drinkTypes}🍾\n"
                                            f"Soni: {count} 🔄\nXisob: {drinkPrice} 💵\n \n"
                                            f"Agar sizga yana boshqa taom kerak bolsa tanlashingiz mumkin"
                                            f" yoki 'Savatcha🛒' bo'limi orqali buyurtma bering ")
            else:
                await bot.send_message(chat_id=user_id,
                                       text=f"Kechirasiz 🍾{drinkName} ning 0.5l turdagi ichimlik yo'q" )



    elif not data.find('delete'):
        dataCall = data.split(" ")
        foodId = dataCall[1]
        base.deleteFoodOfKarzinka(id=foodId)
        await bot.send_message(chat_id=user_id, text=f"Taom ochirildi")



    if not data.find("fastfoodDel"):
        taomlar = base.select_all_foods()
        keys = []
        for taom in (taomlar):
            id = taom[0]
            nomi = taom[1]
            price = taom[2]
            keys.append([InlineKeyboardButton(text=f"{nomi} - {price} 💸", callback_data=f"foods {id}"),
                         InlineKeyboardButton(text="O'chirish", callback_data=f"unsetFood {id}")])

        taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
        await bot.send_message(chat_id=user_id, text="Taomni o'chirish uchun tanlang", parse_mode="markdown", reply_markup=taom_menu)

    elif not data.find("unsetFood"):
        dataCallAdmin = data.split(" ")
        foodIdAdmin = dataCallAdmin[1]
        base.deleteFood(id=foodIdAdmin)
        await bot.send_message(chat_id=user_id, text=f"Taom bazadan o'chirildi")

    elif not data.find("ichimlikDel"):
        taomlar = base.select_all_drinks()
        index = 0
        keys = []
        i = 0
        for taom in (taomlar):
            id = taom[0]
            nomi = taom[1]
            price = taom[2]
            if i % 2 == 0 and i != 0:
                index += 1
            elif i % 2 == 0:
                keys.append([InlineKeyboardButton(text=f"{nomi} - {price} 💸", callback_data=f"foods {id}"),
                             InlineKeyboardButton(text="O'chirish", callback_data=f"unsetDrink {id}")])
        taom_menu = InlineKeyboardMarkup(inline_keyboard=keys)
        await bot.send_message(chat_id=user_id, text="Ichimlikni o'chirish uchun tanlang", parse_mode="markdown",
                                 reply_markup=taom_menu)


    elif not data.find("unsetDrink"):
        dataCallAdmin = data.split(" ")
        foodIdAdmin = dataCallAdmin[1]
        base.deleteDrink(id=foodIdAdmin)
        await bot.send_message(chat_id=user_id, text=f"Ichimlik bazadan o'chirildi")


    elif data == 'fastFoodAdmin':
        await bot.send_message(chat_id=user_id,text="Taom kiriting")
        await Foods.foodName_state.set()

    elif data == 'ichimliklarAdmin':
        await bot.send_message(chat_id=user_id,text="Ichimlikni kiriting")
        await Drink.drinkName_state.set()


    elif not  data.find('foods'):
        count = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="1", callback_data='count ' + data + " 1"),
                    InlineKeyboardButton(text="2", callback_data='count ' + data + " 2")
                ],
                [
                    InlineKeyboardButton(text="3", callback_data='count ' + data + " 3"),
                    InlineKeyboardButton(text="4", callback_data='count ' + data + " 4")
                ],
                [
                    InlineKeyboardButton(text="5", callback_data='count ' + data + " 5"),
                    InlineKeyboardButton(text="6", callback_data='count ' + data + " 6")
                ],
                [
                    InlineKeyboardButton(text="7", callback_data='count ' + data + " 7"),
                    InlineKeyboardButton(text="8", callback_data='count ' + data + " 8")
                ],
                [
                    InlineKeyboardButton(text="9", callback_data='count ' + data + " 9"),
                    InlineKeyboardButton(text="10", callback_data='count ' + data + " 10")
                ]
            ]
        )
        await bot.send_message(chat_id=user_id, text="Sonini tanlang👇", reply_markup=count)
        await message.answer(text="Tanlang..", show_alert=False)


    elif not data.find('ichimliklar'):
            types = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text='0.5L', callback_data='types ' + data + " 0.5L")
                    ],
                    [
                        InlineKeyboardButton(text='1L', callback_data='types ' + data + " 1L")
                    ],
                    [
                        InlineKeyboardButton(text='1.5L', callback_data='types ' + data + " 1.5L")
                    ]
                ]
            )
            await bot.send_message(chat_id=user_id, text="☝ Agar ichimlikning turi faqat 1L bo'lsa\n"
                                                         "1L turini tanlang", reply_markup=types)
            await message.answer(text="Tanlang", show_alert=False)


    elif not  data.find('types'):
        sanash = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="1", callback_data='sanash ' + data + " 1"),
                    InlineKeyboardButton(text="2", callback_data='sanash ' + data + " 2")
                ],
                [
                    InlineKeyboardButton(text="3", callback_data='sanash ' + data + " 3"),
                    InlineKeyboardButton(text="4", callback_data='sanash ' + data + " 4")
                ],
                [
                    InlineKeyboardButton(text="5", callback_data='sanash ' + data + " 5"),
                    InlineKeyboardButton(text="6", callback_data='sanash ' + data + " 6")
                ],
                [
                    InlineKeyboardButton(text="7", callback_data='sanash ' + data + " 7"),
                    InlineKeyboardButton(text="8", callback_data='sanash ' + data + " 8")
                ],
                [
                    InlineKeyboardButton(text="9", callback_data='sanash ' + data + " 9"),
                    InlineKeyboardButton(text="10", callback_data='sanash ' + data + " 10")
                ],
            ]
        )
        await bot.send_message(chat_id=user_id, text="Sonini tanlang👇", reply_markup=sanash)
        await message.answer(text="Tanlang..", show_alert=False)

