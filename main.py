import re

from aiogram import Bot, Dispatcher, executor, types
import logging

from config import API_TOKEN
from fedresurs import Bankrot
from sqlighter import SQLighter
import keyboards

logging.basicConfig(level=logging.INFO)

# инициализация бота
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)

# соединение с БД
db = SQLighter('database/db.db')

# инициализация парсера
fb = Bankrot('lastkey.txt')


async def output(message):
    rec_num = 0
    source, item_num = fb.get_record_details(fb.get_record(rec_num))
    item = fb.form_record_info(source, item_num, rec_num)

    text = 'Тип должника: ' + str(item['Тип должника']) + '\n' \
           + 'Должник: ' + str(item['Должник']) + '\n' \
           + 'Описание: ' + str(item['Описание']) + '\n' \
           + 'Начальная цена: ' + str(item['Начальная цена']) + '\n' \
           + 'Форма торгов: ' + str(item['Форма торгов']) + '\n' \
           + 'Задаток в процентах: ' + str(item['Задаток в процентах']) + '\n' \
           + 'Арбитражный управляющий: ' + str(item['Арбитражный управляющий']) + '\n' \
           + 'Email АУ: ' + str(item['Email АУ']) + '\n' \
           + 'Тел. АУ: ' + str(item['Тел. АУ']) + '\n'

    await bot.send_message(message.chat.id, text)


@dp.callback_query_handler(lambda call_back: call_back.data == "Yes_Stop")
async def stop_bot_parsing(call_back):
    try:
        is_mailing = db.is_mailing(call_back.message.chat.id)
        if is_mailing:
            db.stop_mailing(call_back.message.chat.id)
            await bot.answer_callback_query(call_back.id, text='Работа бота успешно приостановлена!\n'
                                                               'Для возобновления работы напишите:'
                                                               '\n/start.', show_alert=True)
        else:
            await bot.answer_callback_query(call_back.id, text="Бот уже приостановлен.\n"
                                                               "Для возобновления работы напишите:"
                                                               '\n/start.', show_alert=True)
        await bot.edit_message_reply_markup(call_back.message.chat.id, message_id=call_back.message.message_id,
                                            reply_markup=None)
    except Exception as e:
        await bot.send_message(call_back.message.chat.id,
                               'Что-то пошло не так.. Свяжитесь с технической поддержкой')
        print(e)


@dp.callback_query_handler(lambda call_back: call_back.data == 'No_Stop')
async def confirmation_stub(call_back):
    try:
        await bot.answer_callback_query(call_back.id, text='Бот продолжает работу.', show_alert=True)
        await bot.edit_message_reply_markup(call_back.message.chat.id, message_id=call_back.message.message_id,
                                            reply_markup=None)
    except Exception as e:
        await bot.send_message(call_back.message.chat.id,
                               'Что-то пошло не так.. Свяжитесь с технической поддержкой')
        print(e)


@dp.callback_query_handler(lambda call_back: call_back.data == 'add_filter')
async def add_filter(call_back):
    try:
        await bot.send_message(call_back.message.chat.id, 'В разработке.')

    except Exception as e:
        await bot.send_message(call_back.message.chat.id,
                               'Что-то пошло не так.. Свяжитесь с технической поддержкой')
        print(e)


@dp.callback_query_handler(lambda call_back: call_back.data == 'choose_filter')
async def choose_filter(call_back):
    try:
        await bot.answer_callback_query(call_back.id, '')

        filters = []
        filters_id = db.get_filters_ids(call_back.message.chat.id)
        for elem in filters_id:
            user_filter = db.get_filter(elem)
            filter_ = {
                'name': user_filter['filter_name'],
                'id': user_filter['filter_id'],
            }
            filters.append(filter_)
        keyboard = keyboards.my_filters_keyboard(filters)
        await bot.send_message(call_back.message.chat.id, "Выберите фильтр.", reply_markup=keyboard)

    except Exception as e:
        await bot.send_message(call_back.message.chat.id,
                               'Что-то пошло не так.. Свяжитесь с технической поддержкой')
        print(e)


@dp.callback_query_handler(lambda call_back: re.search(r'filter_\d', call_back.data))
async def activate_filter(call_back):
    try:
        new_filter_id = re.search(r'_\d*', call_back.data)
        new_filter_id = re.sub("_", '', new_filter_id.group())
        db.change_active_filter(call_back.message.chat.id, new_filter_id)
        filter_name = db.get_filter(new_filter_id)
        filter_name = filter_name['filter_name']
        await bot.delete_message(call_back.message.chat.id, call_back.message.message_id)
        await bot.send_message(call_back.message.chat.id, f'Фильтр "{filter_name}" был успешно установлен!')

    except Exception as e:
        await bot.send_message(call_back.message.chat.id,
                               'Что-то пошло не так.. Свяжитесь с технической поддержкой')
        print(e)


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    keyboard = keyboards.filter_keyboard()
    if not db.user_exists(message.chat.id):
        await bot.send_message(message.chat.id, 'Добро пожаловать! '
                                                'Вызов меню осуществялется командой: <b><i>/menu</i></b>\n'
                                                'Чтобы приостановить работу бота, воспользуйтесь командой: '
                                                '<b><i>/stop</i></b>',
                               parse_mode='HTML')
        db.add_user(message.chat.id)
        await bot.send_message(message.chat.id,
                               'Похоже, что вы тут впервые. Для начала работы необходимо установить фильтр.',
                               reply_markup=keyboard)
    else:
        if not db.is_mailing(message.chat.id):
            db.start_mailing(message.chat.id)
        await bot.send_message(message.chat.id,
                               'Добро пожаловать! '
                               'Вызов меню осуществялется командой: <b><i>/menu</i></b>\n'
                               'Выберите один из существующих фильтров или создайте новый для начала работы.\n'
                               'Чтобы приостановить работу бота, воспользуйтесь командой: '
                               '<b><i>/stop</i></b>',
                               reply_markup=keyboard, parse_mode='HTML')


@dp.message_handler(commands='menu')
async def print_menu(message: types.Message):
    keyboard = keyboards.menu_keyboard()
    await bot.send_message(message.chat.id, "Выберите интересующий вас пункт меню.", reply_markup=keyboard)


@dp.message_handler(commands="stop")
async def stop_bot(message: types.Message):
    keyboard = keyboards.stop_confirm_keyboard()
    await bot.send_message(message.chat.id, "Вы уверены, что хотите остановить работу бота?", reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
