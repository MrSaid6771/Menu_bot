from aiogram.dispatcher.filters.state import State,StatesGroup

class Malumot(StatesGroup):
    ism_state = State()
    yosh_state = State()
    tel_state = State()
    ish_state = State()
    tasdiqlash = State()

class Foods(StatesGroup):
    foodName_state = State()
    price_state = State()
    gcatalog_state = State()
    status_state = State()
    tasdiqlash_state = State()

class Drink(StatesGroup):
    drinkName_state = State()
    price_1_state = State()
    price_15l_state = State()
    price_1l_state = State()
    price_05l_state = State()
    gcatalog_state = State()
    status_state = State()
    tasdiqlash_state = State()
    litr_state = State()

class Comment(StatesGroup):
    comment_state = State()
    tasdiqlash_state = State()

class Location(StatesGroup):
    jonatish_state = State()
    tasdiqlash_state = State()


class Hisob(StatesGroup):
    tanlash_state = State()
    kun_state = State()
    oy_state = State()