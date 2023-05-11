from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def stop_confirm_buttons():
    buttons = []
    yes_btn = InlineKeyboardButton(text='Да', callback_data='Yes_Stop')
    no_btn = InlineKeyboardButton(text='Нет', callback_data='No_Stop')
    buttons.extend([yes_btn, no_btn])
    return buttons


def stop_confirm_keyboard():
    buttons = stop_confirm_buttons()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def filter_buttons():
    buttons = []
    choose_filter_btn = InlineKeyboardButton(text='Выбрать фильтр', callback_data='choose_filter')
    add_filter_btn = InlineKeyboardButton(text='Добавить новый фильтр', callback_data='add_filter')
    del_filter_btn = InlineKeyboardButton(text="Удалить имеющийся фильтр", callback_data='del_filter')
    buttons.extend([choose_filter_btn, add_filter_btn, del_filter_btn])
    return buttons


def filter_keyboard():
    buttons = filter_buttons()
    keyboard = InlineKeyboardMarkup()
    for btn in buttons:
        keyboard.add(btn)
    return keyboard


def region_buttons(regions):
    buttons = []
    for region in regions:
        btn = KeyboardButton(region)
        buttons.append(btn)
    return buttons


def region_keyboard(regions):
    buttons = region_buttons(regions)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for btn in buttons:
        keyboard.add(btn)
    return keyboard


def tradetypes_buttons(tradetypes):
    buttons = [btn for btn in tradetypes]
    return buttons


def tradetypes_keyboard(tradetypes):
    buttons = tradetypes_buttons(tradetypes)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for btn in buttons:
        keyboard.add(btn)
    return keyboard


def my_filters_buttons(filters):
    buttons = []
    for elem in filters:
        btn = InlineKeyboardButton(text=f"{elem['name']}", callback_data=f"filter_{elem['id']}")
        buttons.append(btn)
    return buttons


def my_filters_keyboard(filters):
    buttons = my_filters_buttons(filters)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for btn in buttons:
        keyboard.add(btn)
    return keyboard


def menu_buttons():
    buttons = []
    start_btn = InlineKeyboardButton(text="Начать поиск.", callback_data="start_search")
    change_filter_btn = InlineKeyboardButton(text="Изменить условия поиска.", callback_data="change_filter")
    trouble_suggestion_btn = InlineKeyboardButton(text="Обратная связь", callback_data='feedback')
    buttons.extend(btn for btn in [start_btn, change_filter_btn, trouble_suggestion_btn]) # генератор нужен?
    return buttons


def menu_keyboard():
    buttons = menu_buttons()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(buttons[0])
    keyboard.add(buttons[1])
    keyboard.add(buttons[2])
    return keyboard
