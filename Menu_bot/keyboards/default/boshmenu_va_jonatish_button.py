from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



buyurtma_tugmasi = ReplyKeyboardMarkup(
    keyboard =[
        [
            KeyboardButton(text='🌭 Buyurtma berish'),
        ],
        [
            KeyboardButton(text="☎ Appetit bila aloqa"),
            KeyboardButton(text="🙋 Jamoamizga qo'shiling"),
        ]
    ],
    resize_keyboard=True
)


menu_tugmasi = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🍔 FastFood'),
            KeyboardButton(text='🍹 Ichimliklar')
        ],
        [
            KeyboardButton(text="Savatcha🛒"),
        ],
        [
            KeyboardButton(text='Buyurtmaga qaytish ↪️')
        ]
    ],
    resize_keyboard=True
)


homeIsAdminPanel = ReplyKeyboardMarkup(
    keyboard =[
        [
            KeyboardButton(text="Qo'shish"),
            KeyboardButton(text="O'chirish")
        ],
        [
            KeyboardButton(text="Bot a'zolari"),
        ]
    ],
    resize_keyboard=True
)

ha_yoq = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ]
    ],
    resize_keyboard=True
)
forKarzinka = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yetkazib berish 🚕", request_location=True),
            KeyboardButton(text="Olib ketish 🏃‍")
        ],
        [
            KeyboardButton("Telefon orqali ☎"),
            KeyboardButton("Commend 📝")

        ],
        [
            KeyboardButton("Orqaga qaytish 👈")
        ]
    ],
    resize_keyboard=True
)

types_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1.5l"),
            KeyboardButton(text="1l"),
            KeyboardButton(text="0.5l"),
        ]
    ],
    resize_keyboard=True
)


litr = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bir litrlik"),
            KeyboardButton(text="Ko'p litrlik")
        ]
    ],
    resize_keyboard=True
)


date = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Hozirgi Kun"),
            KeyboardButton(text="Hozirgi Oy"),
            KeyboardButton(text="Eski hisobot")
        ]
    ],
    resize_keyboard=True
)

date1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kun"),
            KeyboardButton(text="Oy"),
        ]
    ],
    resize_keyboard=True
)