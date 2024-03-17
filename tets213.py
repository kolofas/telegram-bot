text = 'Чеклист уже начат, но еще остались невыполненные пункты:'
import datetime
import json
import logging
import os

import telebot
from telebot import types

logger = telebot.logger
working_directory = os.getcwd()

################################################
################### SETTINGS ###################
################################################
telebot.logger.setLevel(logging.INFO)
TOKEN = '5611948655:AAFWN4vCdqUx7_ZFhfMX4xFouZxj4ZrOGuw'  # '5738278259:AAEeghTOZ-jHGNADdjNtzZS7GIGo7i3WGRo' - оригинальный API
bot = telebot.TeleBot(token=TOKEN)


################################################


def read_file_json(file_name):
    file_name = working_directory + '/' + file_name
    try:
        with open(file_name, 'r') as read_json_file:
            return json.load(read_json_file)
    except FileNotFoundError:
        return {}


def write_file_json(object_python, file_name):
    file_name = working_directory + '/' + file_name
    with open(file_name, 'w') as json_file:
        json.dump(object_python, json_file, indent=4)


################################################
################### DATA #######################
################################################
ROLES = read_file_json('roles.json')
CHECKLISTS = {}
################################################

################################################
################### MARKUPS ####################
################################################
ROLES_MARKUP = types.InlineKeyboardMarkup(row_width=1)
for role_id in ROLES:
    btn = types.InlineKeyboardButton(text=ROLES.get(role_id).get('caption'), callback_data=f'role_{role_id}')
    ROLES_MARKUP.add(btn)

REGISTRATION_MARKUP = types.InlineKeyboardMarkup(row_width=1)
btn_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
REGISTRATION_MARKUP.add(btn_reg)

MAIN_MARKUP = types.InlineKeyboardMarkup(row_width=1)
btn_checklist = types.InlineKeyboardButton(text='Открыть или закрыть смену', callback_data='open_close_shift')
btn_get_users_info = types.InlineKeyboardButton(text='Cписок всех сотрудников', callback_data='get_users_info')
btn_emp_message = types.InlineKeyboardButton(text='Сообщение сотрудникам', callback_data='emps_message')
MAIN_MARKUP.add(btn_checklist, btn_get_users_info, btn_emp_message)


################################################


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    USERS = read_file_json('data_json.json')
    user = USERS.get(str(message.chat.id))
    if user:
        if user.get('role_id'):
            bot.send_message(chat_id=message.chat.id,
                             text=f'Здравствуйте, {user.get("first_name")}! Меню доступных действий ⬇️',
                             reply_markup=MAIN_MARKUP)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f'Здравствуйте, {user.get("first_name")}! Выберите должность:',
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
    USERS = read_file_json('data_json.json')
    USERS[user_id] = {
        'first_name': name[0],
        'last_name': name[-1]
    }

    bot.send_message(chat_id=message.chat.id,
                     text=f'Здравствуйте, {name[0]}! Выберите должность:',
                     reply_markup=ROLES_MARKUP)
    write_file_json(USERS, 'data_json.json')


@bot.callback_query_handler(func=lambda callback: 'role' in callback.data)
def role_select(callback):
    message = callback.message
    user_id = str(message.chat.id)
    role_id = int(callback.data.split('_')[1])
    USERS = read_file_json('data_json.json')
    USERS[user_id]['role_id'] = role_id
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text='Отлично! Меню доступных действий ⬇️',
                          reply_markup=MAIN_MARKUP)
    write_file_json(USERS, 'data_json.json')


@bot.callback_query_handler(func=lambda callback: callback.data == 'go_back')
def return_to_role_select(callback):
    message = callback.message
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=message.message_id,
                          text='Вы вернулись в Главное меню!',
                          reply_markup=MAIN_MARKUP)


@bot.callback_query_handler(func=lambda callback: callback.data == 'emps_message')
def message_to_employees(callback):
    message = callback.message
    user_id = str(message.chat.id)
    USERS = read_file_json('data_json.json')
    role_id = USERS.get(user_id).get('role_id')
    role_id = str(role_id)
    if role_id == '777':
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=message.message_id,
                              text='Запишите сообщение сотрудникам')
        bot.register_next_step_handler(message, send_message_from_admin_to_emp)
    else:
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=message.message_id,
                              text='Вы не можете отправить сообщение',
                              reply_markup=MAIN_MARKUP)


def send_message_from_admin_to_emp(message):
    USERS = read_file_json('data_json.json')
    print(message.text)
    for user_id in USERS:
        user = USERS[user_id]
        if user.get("role_id") == 1:
            bot.send_message(chat_id=user_id,
                             text=message.text)
            bot.send_message(chat_id=message.chat.id,
                             text='Ваше сообщение отправлено!',
                             reply_markup=MAIN_MARKUP)


@bot.callback_query_handler(func=lambda callback: callback.data == 'get_users_info')
def get_users_info(callback):
    message = callback.message
    users_info = ''
    USERS = read_file_json('data_json.json')
    ROLES = read_file_json('roles.json')
    for user_id in USERS:
        user = USERS[user_id]
        users_info += f'*Имя:* {user.get("first_name")} {user.get("last_name")}\n' \
                      f'*Должность:* {ROLES.get(str(user.get("role_id"))).get("caption")}\n' \
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
    if 2 < now_datetime.hour <= 12:
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
        btn_go_back = types.InlineKeyboardButton(
            text='Назад',
            callback_data='go_back'
        )
        markup.add(btn_close, btn_go_back)
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
    all_points = {int(k): v for k, v in all_points.items()}
    done_points = ROLES.get(role_id).get(f'done_points_{action}')
    if done_points:
        points = set(all_points) - set(done_points)
        text = 'Чек-лист уже выполняется'
        write_file_json(ROLES, 'roles.json')
    else:
        points = all_points
        text = 'Начните выполнение чеклиста, выбрав один из пунктов:'
    callback_messages = ROLES.get(role_id).get('callback_messages')
    callback_messages.append((message.message_id, message.chat.id))
    write_file_json(ROLES, 'roles.json')
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
    all_points = ROLES.get(role_id).get(f'all_points_{action}')
    all_points = {int(k): v for k, v in all_points.items()}
    done_points = ROLES.get(role_id).get(f'done_points_{action}')
    if point_id in done_points:
        text = f'Пункт №{point_id} уже был выполнен!'
    else:
        done_points.append(point_id)

    points = set(all_points) - set(done_points)
    write_file_json(ROLES, 'roles.json')
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
        ROLES[role_id]['done_points_open'] = []
        ROLES[role_id]['done_points_close'] = []
        text = f'Чеклист выполнен. Данные отправлены администрации'
    callback_messages = ROLES.get(role_id).get('callback_messages')
    for message in callback_messages:
        bot.edit_message_text(
            chat_id=message[1],
            text=text,
            message_id=message[0],
            reply_markup=markup)
    if not points:
        ROLES[role_id]['callback_messages'] = []
    write_file_json(ROLES, 'roles.json')


bot.infinity_polling()



