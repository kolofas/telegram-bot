import datetime
import json
import logging
import os

import telebot
from telebot import types

logger = telebot.logger
working_directory = os.getcwd() + "/"

################################################
################### SETTINGS ###################
################################################
telebot.logger.setLevel(logging.INFO)
TOKEN =  '5738278259:AAEeghTOZ-jHGNADdjNtzZS7GIGo7i3WGRo' #'5738278259:AAEeghTOZ-jHGNADdjNtzZS7GIGo7i3WGRo'
bot = telebot.TeleBot(token=TOKEN)
################################################

################################################
################### DATA #######################
################################################
ROLES = {
    1: {
        'caption': 'Повар-кассир',
        'all_points_open': {
            1: 'Выключение сигнализации',
            2: 'Включение освещения в зале',
            3: 'Выставление штендера',
            4: 'Проверка зарядки на раб. телефоне',
            5: 'Проверка наличия ингридиентов',
            6: 'Проверка свежести ингридиентов',
            7: 'Подготовка рабочего места',
            8: 'Проверка количества шаурмы и шавермы',
            9: 'Протереть столы в зале дез. ср-вом',
            10: 'Салфетницы, зубочистки, размешиватели, сахар',
            11: 'Бланки тем-ры холод. и мороз. оборудования',
            12: 'Заполнение ежедневного журнала',
            13: 'Проверка жидкого мыла',
            14: 'Проверка бумажных полотенец',
            15: 'Проверка туалетной бумаги'
        },
        'all_points_close': {
            1: 'Убрать ингредиенты в холодильники',
            2: 'Протереть барную стойку',
            3: 'Уборка нижней полки барной стойки',
            4: 'Помыть посуду со средством',
            5: 'Составить посуду (стеллаж)',
            6: 'Кухонные принадлежности (стеллаж)',
            7: 'Помыть раковину',
            8: 'Почистить гриль',
            9: 'Протереть поверхность гриля',
            10: 'Протереть поверхность мороз. камеры',
            11: 'Выключить бытовые приборы',
            12: 'Очистить мусорное ведро',
            13: 'Сухая уборка полов (кухня)',
            14: 'Влажная уборка полов (кухня)',
            15: 'Протереть все столы и стулья (зал)',
            16: 'Очистить мусорное ведро (зал)',
            17: 'Выключить и убрать колонку',
            18: 'Сухая уборка полов (зал)',
            19: 'Влажная уборка полов (зал)',
            20: 'Мусор (туалет)',
            21: 'Помыть унитаз',
            22: 'Проверка туалетной бумаги',
            23: 'Проверка бумажных полотенец',
            24: 'Помыть раковину и зону вокруг',
            25: 'Долить жидкое мыло',
            26: 'Протереть пыль на раме зеркала',
            27: 'Сухая уборка полов (туалет)',
            28: 'Влажная уборка полов (туалет)',
            29: 'Закрыть смену в Presto',
            30: 'Пересчитать наличные в кассе',
            31: 'Заполнение ежедневного отчета',
            32: 'Отправить ежедневный отчет',
            33: 'Выключить компьютер',
            34: 'Выключить ТВ и колонку',
            35: 'Выключить холодильник с напитками',
            36: 'Выключить кондиционер',
            37: 'Выключить тепловую пушку',
            38: 'Выключить свет в туалете',
            39: 'Выключить освещение в зале',
            40: 'Занести штендер',
            41: 'Выключить освещение на улице',
            42: 'Поставить помещение на сигнализацию',
            43: 'Закрыть дверь',
            44: 'Вынести мусор'
        },
        'done_points_open': [],
        'done_points_close': [],
        'callback_messages': []
    },
    777: {
        'caption': 'Владелец'
    },
}

CHECKLISTS = {}
################################################
################################################
################### MARKUPS ####################
################################################


def read_file_json(file_name):
    file_name = working_directory + file_name
    try:
        with open(file_name, 'r') as read_json_file:
            return json.load(read_json_file)
    except FileNotFoundError:
        return {}


def write_file_json(object_python, file_name):
    file_name = working_directory + file_name
    print(file_name)
    with open(file_name, 'w') as json_file:
        json.dump(object_python, json_file, indent=4)

roles_from_json = read_file_json('roles.json')

ROLES_MARKUP = types.InlineKeyboardMarkup(row_width=1)
for role_id in roles_from_json:#ROLES:
    btn = types.InlineKeyboardButton(text=roles_from_json.get(role_id).get('caption'), callback_data=f'role_{role_id}')
    ROLES_MARKUP.add(btn)

REGISTRATION_MARKUP = types.InlineKeyboardMarkup(row_width=1)
btn_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
REGISTRATION_MARKUP.add(btn_reg)

MAIN_MARKUP = types.InlineKeyboardMarkup(row_width=1)
btn_checklist = types.InlineKeyboardButton(text='Открыть или закрыть смену', callback_data='open_close_shift')
btn_get_users_info = types.InlineKeyboardButton(text='Cписок всех сотрудников', callback_data='get_users_info')
MAIN_MARKUP.add(btn_checklist, btn_get_users_info)
################################################


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    USERS = read_file_json('data_json.json')
    print(USERS)
    user = USERS.get(str(message.chat.id))
    if user:
        if user.get('role_id'):
            bot.send_message(chat_id=message.chat.id,
                             text=f'Здравствуйте, {user.get("first_name")}! Меню доступных действий ⬇️',
                             reply_markup=MAIN_MARKUP)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f'Здравствуйте, {user.get("first_navenbme")}! Выберите должность:',
                             reply_markup=ROLES_MARKUP)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Зарегестрируйтесь, чтобы начать выполнение чек-листа',
                         reply_markup=REGISTRATION_MARKUP)


@bot.callback_query_handler(func=lambda callback: callback.data == 'registration')
def registration(callback):
    message = callback.message
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text='Введите ваши имя и фамилию через пробел')
    bot.register_next_step_handler(message, name_input)


def name_input(message):
    user_id = str(message.chat.id)
    name = message.text.split(' ')
    USERS = read_file_json()
    USERS[user_id] = {
        'first_name': name[0],
        'last_name': name[-1]
    }
    bot.send_message(chat_id=message.chat.id,
                     text=f'Здравствуйте, {name[0]}! Выберите должность:',
                     reply_markup=ROLES_MARKUP)
    write_file_json(USERS)



@bot.callback_query_handler(func=lambda callback: 'role' in callback.data)
def role_select(callback):
    message = callback.message
    user_id = str(message.chat.id)
    role_id = int(callback.data.split('_')[1])
    USERS = read_file_json()
    USERS[user_id]['role_id'] = role_id
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text='Отлично! Меню доступных действий ⬇️',
                          reply_markup=MAIN_MARKUP)
    write_file_json(USERS)


@bot.callback_query_handler(func=lambda callback: callback.data == 'get_users_info')
def get_users_info(callback):
    message = callback.message
    users_info = ''
    USERS = read_file_json('data_json.json')
    ROLES = read_file_json('roles.json')
    for user_id in USERS:
        user = USERS[user_id]
        users_info += f'*Имя:* {user.get("first_name")} {user.get("last_name")}\n' \
                     f'*Должность:* {ROLES.get(user.get("role_id")).get("caption")}\n' \
                     f'*Идентификатор:* {user_id}\n\n'
    try:
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=message.message_id,
                              text=users_info,
                              parse_mode='Markdown',
                              reply_markup=MAIN_MARKUP)
    except telebot.apihelper.ApiTelegramException:
        logger.info('Users info was not changed')


@bot.callback_query_handler(func=lambda callback: callback.data == 'open_close_shift')
def open_close_shift(callback):
    message = callback.message
    now_datetime = datetime.datetime.now()
    markup = types.InlineKeyboardMarkup(row_width=1)
    shift_status = f'Текущее время: {now_datetime}.\n'
    if 2 < now_datetime.hour <= 10:
        btn_open = types.InlineKeyboardButton(
            text='Открыть',
            callback_data='open_shift'
        )
        markup.add(btn_open)
        shift_status += 'Откройте'
    # elif 10 < now_datetime.hour <= 21:
    #     markup = MAIN_MARKUP
    #     shift_status += 'Cейчас нельзя открыть или закрыть'
    else:
        btn_close = types.InlineKeyboardButton(
            text='Закрыть',
            callback_data='close_shift'
        )
        markup.add(btn_close)
        shift_status += 'Закройте'
    bot.edit_message_text(
        chat_id=message.chat.id,
        text=f'{shift_status} смену',
        message_id=message.message_id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda callback: callback.data in ('open_shift', 'close_shift'))
def process_shift(callback):
    message = callback.message
    user_id = str(message.chat.id)
    USERS = read_file_json('data_json.json')
    ROLES = read_file_json('roles.json')
    role_id = USERS.get(user_id).get('role_id')
    role_id = str(role_id)
    action = callback.data.split('_')[0]
    all_points = ROLES.get(role_id).get(f'all_points_{action}')
    done_points = ROLES.get(role_id).get(f'done_points_{action}')
    if done_points:
        points = set(all_points) - set(done_points)
        text = 'Чеклист уже начат, но еще остались невыполненные пункты:'
    else:
        points = all_points
        text = 'Начните выполнение чеклиста, выбрав один из пунктов:'
    callback_messages = ROLES.get(role_id).get('callback_messages')
    callback_messages.append(message)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for point_id in points:
        btn = types.InlineKeyboardButton(
            text=f'{point_id}. {all_points[point_id]}',
            callback_data=f'{action}_point_{point_id}'
        )
        markup.add(btn)
    bot.edit_message_text(
        chat_id=message.chat.id,
        text=text,
        message_id=message.message_id,
        reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: 'point' in callback.data)
def process_point(callback):
    message = callback.message
    user_id = str(message.chat.id)
    USERS = read_file_json('data_json.json')
    ROLES = read_file_json('roles.json')
    role_id = USERS.get(user_id).get('role_id')
    role_id = str(role_id)
    action = callback.data.split('_')[0]
    point_id = int(callback.data.split('_')[-1])
    all_points = ROLES.get(role_id) .get(f'all_points_{action}')
    done_points = ROLES.get(role_id).get(f'done_points_{action}')
    if point_id in done_points:
        text = f'Пункт №{point_id} уже был выполнен!'
    else:
        done_points.append(point_id)
    points = set(all_points) - set(done_points)
    print(all_points[str(point_id)])
    print(done_points)
    if points:
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_point_id in points:
            btn = types.InlineKeyboardButton(
                text=f'{btn_point_id}. {all_points[btn_point_id]}',
                callback_data=f'{action}_point_{btn_point_id}'
            )
            markup.add(btn)
        text = f'{point_id} - готово!'

    else:
        markup = MAIN_MARKUP
        for admin_user_id in USERS:
            if USERS.get(admin_user_id).get('role_id') == 777:
                bot.send_message(chat_id=admin_user_id,
                                 text=f'Здравствуйте, {USERS.get(admin_user_id).get("first_name")}! Был выполнен чеклист ⬇️',
                                 reply_markup=markup)
        text = f'Чеклист выполнен. Данные отправлены администрации'
    callback_messages = ROLES.get(role_id).get('callback_messages')
    for message_inst in callback_messages:
        bot.edit_message_text(
            chat_id=message_inst.chat.id,
            text=text,
            message_id=message_inst.message_id,
            reply_markup=markup)


bot.infinity_polling()
