import datetime
import json
import logging
import sqlite3 as das

import telebot
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

TOKEN = '5611948655:AAFWN4vCdqUx7_ZFhfMX4xFouZxj4ZrOGuw'
bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    # conn = das.connect('db.sqlite')
    # cur = conn.cursor()

    # cur.execute('SELECT * FROM chats WHERE chat_id=?', (message.chat.id,))
    # chat = cur.fetchone()
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn_reg = types.InlineKeyboardButton(text='Регистрация',
                                         callback_data='registration')
    kb.add(btn_reg)
    bot.send_message(message.chat.id, 'Нажми кнопку для регистрации',
                     reply_markup=kb)


@bot.callback_query_handler(func=lambda callback: callback.data)
def registration_in_database(callback):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT role_id FROM roles;')
    roles_ids_cort = cur.fetchall()
    roles_ids_list = [roles_ids_cort[0] for roles_ids_cort in roles_ids_cort]
    print(roles_ids_list, 'roles_ids_list')
    num = callback.data
    chat_id = callback.message.chat.id
    if num == 'registration': # Обработка коллбека на регистрацию
        bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id,
                         text='Теперь мне необходимо получить от тебя имя и фамилию')
    elif num in ['open', 'close']:
        print('open / close success')
        markup = open_close_shift(chat_id)
        bot.edit_message_text(chat_id=chat_id,
                              message_id=callback.message.message_id,
                              text='Чеклист',  reply_markup=markup)
    elif 'point_' in num:
        #TODO: Здесь я делаю запрос к базе и нахожу чек-лист, если он есть, то его checklist_id передаю в функцию point_checklist
        checklist_test_id = test_checklist_id(chat_id)
        if checklist_test_id:
            markup = point_checklist(chat_id, num, callback.message.message_id, checklist_test_id)
            print('point success', num)
            print(checklist_test_id)
        else:
            print('ЛОХ')


    elif int(num) in roles_ids_list: # Обработка коллбека на выбор роли
        markup = choose_role(num, chat_id)
        print('success')
        bot.edit_message_text(
            chat_id=chat_id,
            text='Нажми кнопку открыть / закрыть смену',
            message_id=callback.message.message_id,
            reply_markup=markup
        )


@bot.message_handler(content_types=['text'])
def name_send_to_database(message):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM chats WHERE chat_id=?', (message.chat.id,))
    chat = cur.fetchone()
    if chat:
        print('CHAT:', chat)
    else:
        chat_id = message.chat.id
        first_name, last_name = str(message.text).split(' ')
        cur.execute('INSERT INTO chats VALUES(?, ?, ?, ?);',
                    (chat_id, first_name, last_name, None))
        conn.commit()
        cur.execute('SELECT caption, role_id FROM roles')
        captions = cur.fetchall()
        print(captions)
        kb_roles = types.InlineKeyboardMarkup(row_width=1)
        for caption in captions:
            btn_role = types.InlineKeyboardButton(
                text=caption[0],
                callback_data=caption[1]
            )
            kb_roles.add(btn_role)
        bot.send_message(
            chat_id=message.chat.id,
            text='Выбери должность',
            reply_markup=kb_roles
        )



def choose_role(role_id, chat_id):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    role_callback = int(role_id)
    print(type(role_callback))
    cur.execute('SELECT role_id FROM roles;')
    role_id_cort = cur.fetchall()
    role_ids = [role_id_cort[0] for role_id_cort in role_id_cort]
    print(role_ids)
    if role_callback in role_ids:
        print('go update')
        cur.execute('UPDATE chats SET role_id=? WHERE chat_id=?;', (role_callback,
                                                                    chat_id,))
        conn.commit()
    kb_open_close = types.InlineKeyboardMarkup(row_width=1)
    if datetime.datetime.now().hour < 10:
        btn_open = types.InlineKeyboardButton(
            text='Открыть смену',
            callback_data='open'
        )
        kb_open_close.add(btn_open)
    else:
        btn_close = types.InlineKeyboardButton(
            text='Закрыть смену',
            callback_data='close'
        )
        kb_open_close.add(btn_close)
    return kb_open_close


def open_close_shift(chat_id):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT role_id FROM chats WHERE chat_id=?', (chat_id,))
    role_id = cur.fetchone()
    cur.execute('SELECT text, point_id FROM checklist_points WHERE role_id=?', (role_id[0],))
    points_texts = cur.fetchall()
    list_points_done = json.dumps([])
    kb_start_of_checklist = types.InlineKeyboardMarkup(row_width=1)
    for point_text in points_texts:
        item = types.InlineKeyboardButton(
            text=point_text[0],
            callback_data=f'point_{point_text[1]}'
        )
        kb_start_of_checklist.add(item)
    cur.execute('INSERT INTO checklists(chat_id, points_done_json, creation_datetime) VALUES (?, ?, ?);',
                (chat_id, list_points_done, datetime.datetime.now(tz=None)))
    conn.commit()
    return kb_start_of_checklist


def point_checklist(chat_id, callback_data, message_id, checklist_id):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT role_id FROM chats WHERE chat_id=?', (chat_id,))
    role_id = cur.fetchone()
    point_id_callback = int(callback_data.split('_')[1])

    cur.execute('SELECT * FROM checklists WHERE checklist_id=?', (checklist_id,))
    checklist = cur.fetchone()
    print(checklist, 'checklist!!!!')
    set_points_from_db = json.loads(checklist[2])
    cur.execute('SELECT point_id FROM checklist_points WHERE point_id=?', (point_id_callback,))
    done_point_id = cur.fetchone()
    set_points_from_db.append(done_point_id[0])
    set_points_to_json_data = json.dumps(set_points_from_db)

    cur.execute('SELECT point_id FROM checklist_points WHERE role_id=?', (role_id[0],))
    points_ids_db = cur.fetchall()
    list_points_ids = [point_id_db[0] for point_id_db in points_ids_db]
    print(list_points_ids)
    cur.execute('UPDATE checklists SET points_done_json=?, update_datetime=? WHERE checklist_id=?;',
                (set_points_to_json_data, datetime.datetime.now(),
                 checklist[0],))
    conn.commit()

    markup_points_ids = set(list_points_ids) - set(set_points_from_db)
    print(markup_points_ids, set(list_points_ids), set(set_points_from_db))
    kb_points = types.InlineKeyboardMarkup(row_width=1)
    if not markup_points_ids:
        cur.execute('SELECT chat_id FROM chats WHERE role_id=777')
        admins = cur.fetchall()
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'Чеклист пройден {checklist[0]}',
            reply_markup=None
        ) #TODO: callback должен принимать не только chat_id, но и checklist_id
        for admin in admins:
            cur.execute('SELECT first_name, last_name FROM chats WHERE chat_id=?', (chat_id,))
            name = cur.fetchone()
            bot.send_message(
                chat_id=admin[0],
                text=f'Сотрудник {name[0]} {name[1]} выполнил чек-лист')
    else:
        for point_id in markup_points_ids:
            cur.execute('SELECT text FROM checklist_points WHERE point_id=?', (point_id,))
            point_text = cur.fetchone()
            btn_points = types.InlineKeyboardButton(
                text=point_text[0],
                callback_data=f'point_{point_id}'
            )
            kb_points.add(btn_points)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f'{callback_data} - готово!',
            reply_markup=kb_points
        )

    return kb_points


def test_checklist_id(chat_id):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT checklist_id FROM checklists WHERE chat_id=?', (chat_id,))
    checklist_id = cur.fetchone()
    if checklist_id:
        return checklist_id[0]
    else:
        return False

# TODO: модифицируется таблица, где содержатся вопросы для чек-листов, там будет маркер(True, False - на открытие и закрытие смены)

bot.infinity_polling()





# TODO: Созвон с Димасом - делаем общий отчет со временем начала прохождения чек-листа и когда закончил чек-лист, также добавляются фотографии в сообщении передача Димону и администратору

# TODO: 1. Проверка наличия чек-листа в базе, если он есть, то я его передаю в функцию point_checklist
# TODO: 1.1. Все должно работать также, только чек-лист могут пройти несколько человек
# TODO: 2. Надо поменять сообщение, которое отправляется владельцу, а то что чек-лист по такой-то должности выполнен

