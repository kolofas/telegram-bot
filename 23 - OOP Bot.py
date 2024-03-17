import datetime
import json
import logging
import os
import telebot
from telebot import types


logger = telebot.logger
working_directory = os.getcwd()

# bot_name = https://t.me/real_cool_bobot
# settings
logger.setLevel(logging.INFO)


class FileDoer:
    def __init__(self, file_name):
        self.file_name = working_directory + '/' + file_name

    def read_json(self):
        try:
            with open(self.file_name, 'r') as read_json:
                return json.load(read_json)
        except FileNotFoundError:
            return {}

    def write_file_json(self, object_python):
        with open(self.file_name, 'w') as json_file:
            json.dump(object_python, json_file, indent=4)


data_users = FileDoer('data_json.json')
data_roles = FileDoer('roles.json')
checklists = {}


class Users:
    def __init__(self):
        self.users = data_users.read_json()

    def get(self, message):
        return self.users.get(message)


users = Users()


# roles_markup
roles_markup = types.InlineKeyboardMarkup(row_width=1)
roles = data_roles.read_json()
for role_id in roles:
    btn_role = types.InlineKeyboardButton(text=roles.get(role_id).get('caption'), callback_data=f'role_{role_id}')
    roles_markup.add(btn_role)
# roles_markup

# registration_markup
registration_markup = types.InlineKeyboardMarkup(row_width=1)
btn_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
registration_markup.add(btn_reg)
# registration_markup


# main_markup
main_markup = types.InlineKeyboardMarkup(row_width=1)
btn_checklist = types.InlineKeyboardButton(text='Открыть или закрыть смену', callback_data='open_close_shift')
btn_get_users_info = types.InlineKeyboardButton(text='Список всех сотрудников', callback_data='get_users_info')
btn_emp_message = types.InlineKeyboardButton(text='Сообщение сотрудникам', callback_data='emps_message')
main_markup.add(btn_checklist, btn_get_users_info, btn_emp_message)
# main_markup


class MyBot:
    def __init__(self):
        self.token = '6285449365:AAHtq0XMvmf6YeoeRiNBsaexZL5_1iIwilc'
        self.bot = telebot.TeleBot(self.token)

        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            user = users.get(str(message.chat.id))
            print(user)
            if user:
                if user.get('role_id'):
                    self.bot.send_message(chat_id=message.chat.id,
                                          text=f'Привет, {user.get("first_name")}! Меню:',
                                          reply_markup=main_markup)
                else:
                    self.bot.send_message(chat_id=message.chat.id,
                                          text=f'Привет! {user.get("first_name")}! Выбери должность:',
                                          reply_markup=roles_markup)
            else:
                self.bot.send_message(chat_id=message.chat.id,
                                      text='Зарегистрируйтесь, чтобы начать выполнение чек-листа',
                                      reply_markup=registration_markup)

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'registration')
        def registration(callback):
            message = callback.message
            self.bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=message.message_id,
                                        text='Введи свое имя и фамилию через пробел')
            self.bot.register_next_step_handler(message, name_input)

        def name_input(message):
            user_id = str(message.chat.id)
            name = message.text.split(' ')
            users = data_users.read_json()
            users[user_id] = {
                'first_name': name[0],
                'last_name': name[-1]
            }
            self.bot.send_message(chat_id=message.chat.id,
                                  text=f'Привет, {name[0]}! Выберите должность:',
                                  reply_markup=roles_markup)
            data_users.write_file_json(users)

        @self.bot.callback_query_handler(func=lambda callback: 'role' in callback.data)
        def role_select(callback):
            message = callback.message
            user_id = str(message.chat.id)
            role_id = int(callback.data.split('_')[1])
            users = data_users.read_json()
            users[user_id]['role_id'] = role_id
            self.bot.edit_message_text(chat_id=message.chat.id,
                                           message_id=message.message_id,
                                           text='Вы вернулись в главное меню!',
                                           reply_markup=main_markup)

        @self.bot.callback_query_handler(func=lambda callback: callback.data == 'open_close_shift')
        def open_close_shift(callback):
            message = callback.message
            now_datetime = datetime.datetime.now()
            markup_shift = types.InlineKeyboardMarkup(row_width=1)
            shift_status = f'Текущее время: {now_datetime}.\n'
            if 2 < now_datetime.hour <= 12:
                btn_open = types.InlineKeyboardButton(text='Открыть', callback_data='open_shift')
                markup_shift.add(btn_open)
                shift_status += 'Откройте'
            else:
                btn_close = types.InlineKeyboardButton(text='Закрыть', callback_data='close_shift')
                btn_go_back = types.InlineKeyboardButton(text='Назад', callback_data='go_back')
                markup_shift.add(btn_close, btn_go_back)
                shift_status += 'Закройте'
            self.bot.edit_message_text(chat_id=message.chat.id,
                                           text=f'{shift_status} смену',
                                           message_id=message.message_id,
                                           reply_markup=markup_shift)

    def run(self):
        self.bot.polling()


if __name__ == '__main__':
    my_bot = MyBot()
    my_bot.run()




# # roles_markup
# ROLES_MARKUP = types.InlineKeyboardMarkup(row_width=1)
# for role_id in ROLES:
#     btn = types.InlineKeyboardButton(text=ROLES.get(role_id).get('caption'), callback_data=f'role_{role_id}')
#     ROLES_MARKUP.add(btn)
# # roles_markup
#
# # registration_markup
# REGISTRATION_MARKUP = types.InlineKeyboardMarkup(row_width=1)
# btn_reg = types.InlineKeyboardButton(text='Регистрация', callback_data='registration')
# REGISTRATION_MARKUP.add(btn_reg)
# # registration_markup
#
# # main_markup
# MAIN_MARKUP = types.InlineKeyboardMarkup(row_width=1)
# btn_checklist = types.InlineKeyboardButton(text='Открыть или закрыть смену', callback_data='open_close_shift')
# btn_get_users_info = types.InlineKeyboardButton(text='Cписок всех сотрудников', callback_data='get_users_info')
# btn_emp_message = types.InlineKeyboardButton(text='Сообщение сотрудникам', callback_data='emps_message')
# MAIN_MARKUP.add(btn_checklist, btn_get_users_info, btn_emp_message)
# # main_markup




