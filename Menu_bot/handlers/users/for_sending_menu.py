import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from states.ishga_qabul import Location

from keyboards.default.boshmenu_va_jonatish_button import *
from loader import dp, base, bot
from states.ishga_qabul import Comment


@dp.message_handler(text='🌭 Buyurtma berish')
async def bot_echo(message: types.Message):
    await message.answer(text='Taomni tanlang 🍔🌮', reply_markup=menu_tugmasi)

@dp.message_handler(text='Buyurtmaga qaytish ↪️')
async def bot_echo(message: types.Message):
    await message.answer(text='Buyurtma Tugmasi', reply_markup=buyurtma_tugmasi)


@dp.message_handler(text='☎ Appetit bila aloqa')
async def bot_echo(message: types.Message):
    number = "+998999091012"
    await message.answer(text=f"Biz bilan bog'lanish uchun \n📞{number}\n"
                              f"E'tibor uchun raxmat")


@dp.message_handler(text="Orqaga qaytish 👈")
async def bot_echo(message: types.Message):
    await message.answer(text="Taomlar tugmasi", reply_markup=menu_tugmasi)

#################################### FOR COMMEND #######################################################################

@dp.message_handler(text="Commend 📝")
async def bot_echo(message: types.Message):
    await message.answer(text="Taomingiz uchun commendni yozing")
    await Comment.comment_state.set()

@dp.message_handler(state=Comment.comment_state)
async def send_order(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data({"comment": comment})
    inform = await state.get_data()
    comment = inform.get('comment')
    text = f"✅Commend:  {comment}\n"
    await message.answer(text=f"Ma'lumotingiz tasdiqlaysizmi ✅")
    await message.answer(text=text, reply_markup=ha_yoq)
    await Comment.tasdiqlash_state.set()

@dp.message_handler(state=Comment.tasdiqlash_state,text="Ha")
async def bot_echo(message: types.Message, state: FSMContext):
    userId = message.from_user.id
    inform = await state.get_data()
    comment = inform.get('comment')
    select = base.selectKarzinka(user_id=userId)
    for update in select:
        orderId = update[0]
        base.orderUpdateKarzinka(id=orderId, commend=comment)
    await message.answer(text="Malumotingiz tasdiqlandi ✅", reply_markup=forKarzinka)
    await state.finish()

@dp.message_handler(state=Comment.tasdiqlash_state,text="Yo'q")
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(text="Bekor qilindi", reply_markup=menu_tugmasi)
    await state.finish()

########################## FOR GETTING LOCATION #########################################################################

@dp.message_handler(content_types=ContentType.LOCATION)
async def send_order(message: types.Message, state: FSMContext):
    await message.answer(text='Locatsiyangizni tasdiqlaysizmi ✅\n\n'
                              'Eslatib o\'tamiz Yetkazib berish xizmatimiz 5️⃣0️⃣0️⃣0️⃣ So\'m', reply_markup=ha_yoq)
    await Location.jonatish_state.set()
    location1 = message.location.latitude
    location2 = message.location.longitude
    await state.update_data({"location1": location1})
    await state.update_data({"location2": location2})

@dp.message_handler(state=Location.jonatish_state, text="Ha")
async def send_order(message: types.Message, state: FSMContext):
    order = base.selectAllKarzinka()
    if len(order) != 0:
        await message.answer( text=' Locatsiya tasdiqlandi 📥',  reply_markup=menu_tugmasi)
        inform = await state.get_data()
        locat1 = inform.get('location1')
        locat2 = inform.get('location2')

        await bot.send_location(chat_id='-890620966', latitude=locat1, longitude=locat2)
        await state.finish()
        full_name = message.from_user.full_name
        text = f"✅Mijoz: {full_name}"

        await bot.send_message(chat_id='-890620966',text=text)
        await state.finish()
###########################Yetkazib berish tugmasi uchun print qilish###################################################
        if len(full_name) != 0:
            for forOrder in order:
                username = message.from_user.full_name
                user_id = forOrder[1]
                nameFood = forOrder[2]
                countOrder = forOrder[3]
                summa = forOrder[4]
                drinkType = forOrder[6]
                catalogOrder = forOrder[7]
                forCommend = forOrder[8]
                base.orderAdd(user_id=user_id, name=nameFood, price=summa, count=countOrder, catalog=catalogOrder, type=drinkType,
                              commend=forCommend, user_name=username)
            y = datetime.datetime.now()
            vaqt = y.strftime("%X")
            number = "+998999091012"
            await message.answer(text=f"Mahsulotingiz ⌚ {vaqt}-da buyurtma berildi, biz bilan aloqada bo'lib turing\n\n"
                                      f"Bog'lanish uchun \n📞{number}\n", reply_markup=menu_tugmasi)
            select = base.selectAllKarzinka()
            for take in select:
                userId = take[1]
                name = take[2]
                count = take[3]
                price = take[4]
                types = take[6]
                catalog = take[7]
                x = datetime.datetime.now()
                vaqtDay = x.strftime("%d")
                vaqtMonth = x.strftime('%m')
                base.addForArxiv(user_id=userId, ordername=name, price=price, count=count, types=types, catalog=catalog, day=vaqtDay, month=vaqtMonth)

                base.deleteOrders(user_id=userId)
                base.deleteKarzinka(user_id=userId)
    else:
        await message.answer(text='Karzinkada hech narsa yo\'q, buyurtma bering', reply_markup=menu_tugmasi)

@dp.message_handler(state=Location.jonatish_state, text="Yo'q")
async def send_order(message: types.Message, state: FSMContext):
    await message.answer(text='Ma\'lumotlaringizni qaytadan kiriting',reply_markup=menu_tugmasi)
    await state.finish()

##################### FOR SENDING TO ORDER #############################################################################

@dp.message_handler(text="Olib ketish 🏃‍")
async def send_order(message: types.Message):
    order = base.selectAllKarzinka()
    if len(order) != 0:
        for forOrder in order:
            username = message.from_user.full_name
            user_id = forOrder[1]
            nameFood = forOrder[2]
            countOrder = forOrder[3]
            summa = forOrder[4]
            drinkType = forOrder[6]
            catalogOrder = forOrder[7]
            forCommend = forOrder[8]
            base.orderAdd(user_id=user_id, name=nameFood, price=summa, count=countOrder, catalog=catalogOrder, type=drinkType,
                          commend=forCommend, user_name=username)
        y = datetime.datetime.now()
        vaqt = y.strftime("%X")
        number = "+998999091012"
        await message.answer(text=f"Mahsulotingiz ⌚ {vaqt}-da buyurtma berildi, biz bilan aloqada bo'lib turing\n\n"
                                  f"Bog'lanish uchun \n📞{number}\n",reply_markup=menu_tugmasi)
        select = base.selectAllKarzinka()
        for take in select:
            userId = take[1]
            name = take[2]
            count = take[3]
            price = take[4]
            types = take[6]
            catalog = take[7]
            x = datetime.datetime.now()
            vaqtDay = x.strftime("%d")
            vaqtMonth = x.strftime('%m')
            base.addForArxiv(user_id=userId, ordername=name, price=price, count=count, types=types, catalog=catalog, day=vaqtDay,
                             month=vaqtMonth)
            base.deleteOrders(user_id=userId)
            base.deleteKarzinka(user_id=userId)
    else:
        await message.answer(text='Karzinkada hech narsa yo\'q, buyurtma bering', reply_markup=menu_tugmasi)

##################### FOR CALLING ######################################################################################

@dp.message_handler(text='Telefon orqali ☎')
async def bot_echo(message: types.Message):
    number = "+998999091012"
    await message.answer(text=f"Buyurtma berish uchun \n📞{number}\n"
                              f"Murojaat uchun raxmat")

