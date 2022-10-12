import datetime
import json
import logging
import sqlite3 as das

import telebot
from telebot import types

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

TOKEN = '5551612391:AAG5wW3JmWZQr1e0bFibfVouv708_9Qlzkg'
bot = telebot.TeleBot(token=TOKEN)

button_open_shift = types.KeyboardButton('Открыть смену')
button_close_shift = types.KeyboardButton('Закрыть смену')


@bot.message_handler(commands=['start'])
def start_command(message):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()

    cur.execute("SELECT * FROM chats WHERE chat_id=?", (message.chat.id,))
    chat = cur.fetchone()
    print(chat)
    if chat:
        if chat[3]:
            markup_logged_common = types.ReplyKeyboardMarkup(resize_keyboard=True)
            if datetime.datetime.now().hour < 10:
                markup_logged_common.add(button_open_shift)
            else:
                markup_logged_common.add(button_close_shift)
            bot.send_message(chat_id=message.chat.id,
                             text='Смена',
                             reply_markup=markup_logged_common)
        else:
            cur.execute("SELECT caption FROM roles")
            captions = cur.fetchall()
            markup_roles = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for caption in captions:
                item = types.KeyboardButton(caption[0])
                markup_roles.add(item)
            bot.send_message(chat_id=message.chat.id,
                             text='Выбери свою должность',
                             reply_markup=markup_roles) #TODO: Вот здесь уже должен передаваться callback
            #TODO: понять, на какие кнопки можно вешать Callback функции, переделать часть функционала на callback
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Привет! Для регистрации отправь мне свои имя и фамилию через пробел')




@bot.message_handler(content_types=['text'])
def message_reply(message):
    conn = das.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute("SELECT * FROM chats WHERE chat_id=?", (message.chat.id,))
    chat = cur.fetchone()
    if chat:
        print('CHAT:', chat)
        if chat[3]:
            cur.execute("SELECT text FROM checklist_points where role_id=?", (chat[3],))
            texts_cort = cur.fetchall()
            texts = [text_cort[0] for text_cort in texts_cort]
            if message.text in ['Открыть смену', 'Закрыть смену']:
                cur.execute("SELECT role_id FROM chats WHERE chat_id=?", (message.chat.id,))
                role_id = cur.fetchone()
                cur.execute("SELECT text FROM checklist_points WHERE role_id=?", (role_id[0],))
                points_texts = cur.fetchall()
                markup_points = types.ReplyKeyboardMarkup(resize_keyboard=True)
                list_points_done = json.dumps([])
                for point_text in points_texts:
                    item = types.KeyboardButton(point_text[0])
                    markup_points.add(item)
                bot.send_message(chat_id=message.chat.id,
                                 text='Чеклист',
                                 reply_markup=markup_points)
                cur.execute("INSERT INTO checklists(chat_id, points_done_json, creation_datetime) VALUES (?, ?, ?);",
                            (message.chat.id, list_points_done, datetime.datetime.now(
                                tz=None)))  # в этом моменте создается чек-лист, тут ничего не должно передавать в points_done_json
                conn.commit()
            elif message.text in texts:
                cur.execute("SELECT role_id FROM chats WHERE chat_id=?", (message.chat.id,))
                role_id = cur.fetchone()
                cur.execute("SELECT text FROM checklist_points WHERE role_id=?", (role_id[0],))
                points_texts = cur.fetchall()

                cur.execute("SELECT * FROM checklists WHERE chat_id=?", (message.chat.id,))
                checklist = cur.fetchone()
                # cur.execute("SELECT points_done_json FROM checklists WHERE checklist_id=?", checklist_id)
                # points_from_db = cur.fetchone()
                print(checklist)
                set_points_from_db = json.loads(checklist[2])
                cur.execute("SELECT point_id FROM checklist_points WHERE role_id=?", (role_id[0],))
                points_ids_db = cur.fetchall()
                points_ids = [point_id_db[0] for point_id_db in points_ids_db]

                cur.execute("SELECT point_id FROM checklist_points WHERE text=?", (message.text,))
                done_point_id = cur.fetchone()  # достать из кортежа
                set_points_from_db.append(done_point_id[0])  # достал
                set_points_json_data = json.dumps(set_points_from_db)
                cur.execute("UPDATE checklists SET points_done_json=?, update_datetime=? WHERE checklist_id=?;",
                            (set_points_json_data, datetime.datetime.now(),
                             checklist[0],))
                conn.commit()
                markup_points_ids = set(points_ids) - set(set_points_from_db)
                print(markup_points_ids, set(points_ids), set(set_points_from_db))
                if not markup_points_ids:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'Чек-лист пройден {checklist[0]}')
                else:
                    markup_points = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    for point_id in markup_points_ids:
                        cur.execute("SELECT text FROM checklist_points WHERE point_id=?", (point_id,))
                        point_text = cur.fetchone()
                        item = types.KeyboardButton(point_text[0])
                        markup_points.add(item)
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'{message.text} - готово',
                                     reply_markup=markup_points)
            else:
                cur.execute("SELECT * FROM roles where role_id=?", (chat.role_id,))
                role = cur.fetchone()
                markup_logged_common = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if datetime.datetime.now().hour < 10:
                    markup_logged_common.add(button_open_shift)
                else:
                    markup_logged_common.add(button_close_shift)
                bot.send_message(chat_id=message.chat.id,
                                 text=f'Ты уже зарегестрирован в системе, как '
                                      f'{role[1]} {chat[1]} {chat[2]}!',
                                 reply_markup=markup_logged_common)
        else: #TODO: отсюда и
            cur.execute("SELECT caption FROM roles;")
            captions_cort = cur.fetchall()
            captions = [caption_cort[0] for caption_cort in captions_cort]
            if message.text in captions:
                cur.execute("SELECT role_id FROM roles where caption=?", (message.text,))
                role_id = cur.fetchone()[0]
                cur.execute("UPDATE chats SET role_id=? WHERE chat_id=?;", (role_id, message.chat.id,))
                conn.commit()
                markup_logged_common = types.ReplyKeyboardMarkup(resize_keyboard=True)
                if datetime.datetime.now().hour < 10:
                    markup_logged_common.add(button_open_shift)
                else:
                    markup_logged_common.add(button_close_shift)
                bot.send_message(chat_id=message.chat.id,
                                 text='Смена',
                                 reply_markup=markup_logged_common)
            else:
                cur.execute("SELECT caption FROM roles")
                captions = cur.fetchall()
                markup_roles = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for caption in captions:
                    item = types.KeyboardButton(caption[0])
                    markup_roles.add(item)
                bot.send_message(chat_id=message.chat.id,
                                 text='Не знаю такой команды. Выбери свою должность',
                                 reply_markup=markup_roles)
                # TODO: и досюда, все должно перейти в callback
    else:
        chat_id = message.chat.id
        first_name, last_name = str(message.text).split(' ')
        cur.execute("INSERT INTO chats VALUES(?, ?, ?, ?);",
                    (chat_id, first_name, last_name, None))
        conn.commit()
        cur.execute("SELECT caption FROM roles")
        captions = cur.fetchall()
        markup_roles = types.ReplyKeyboardMarkup(resize_keyboard=True) #TODO: здесь уже будет создан первый inline markup с коллбеком
        for caption in captions:
            item = types.KeyboardButton(caption[0])
            markup_roles.add(item)
        bot.send_message(chat_id=message.chat.id,
                         text='Выбери свою должность',
                         reply_markup=markup_roles)


@bot.message_handler(content_types=['photo'])
def photo_reply(message):
    photo = message.photo[-1]
    print(photo)
    bot.send_message(chat_id=message.chat.id,
                     text=photo.file_id)


bot.infinity_polling()
