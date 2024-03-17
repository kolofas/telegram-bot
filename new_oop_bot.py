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


class MyPot:
    def __init__(self):
        self.token = <TOKEN>
        self.bot = telebot.TeleBot(self.token)
        self.welcome = self.bot.message_handler(commands=['start'])(self.welcome)
        self.registration = self.bot.callback_query_handler(func=lambda callback: callback.data == 'registration')(self.registration)
        self.role_select = self.bot.callback_query_handler(func=lambda callback: 'role' in callback.data)(self.role_select)
        self.open_close_shift = self.bot.callback_query_handler(func=lambda callback: callback.data == 'open_close_shift')(self.open_close_shift)
        self.process_shift = self.bot.callback_query_handler(func=lambda callback: callback.data in ('open_shift', 'close_shift'))(self.process_shift)
        self.process_point = self.bot.callback_query_handler(func=lambda callback: 'point' in callback.data)(self.process_point)

    def welcome(self, message):
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

    def registration(self, callback):
        message = callback.message
        self.bot.edit_message_text(chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   text='Введи свое имя и фамилию через пробел')
        self.bot.register_next_step_handler(message, self.name_input)

    def name_input(self, message):
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

    def role_select(self, callback):
        message = callback.message
        user_id = str(message.chat.id)
        role_id = int(callback.data.split('_')[1])
        users = data_users.read_json()
        users[user_id]['role_id'] = role_id
        self.bot.edit_message_text(chat_id=message.chat.id,
                                   message_id=message.message_id,
                                   text='Вы вернулись в главное меню!',
                                   reply_markup=main_markup)
        data_users.write_file_json(users)

    def open_close_shift(self, callback):
        message = callback.message
        now_datetime = datetime.datetime.now()
        markup_shift = types.InlineKeyboardMarkup(row_width=1)
        shift_status = f'Текущее время: {now_datetime}. \n'
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

    def process_shift(self, callback):
        message = callback.message
        user_id = str(message.chat.id)
        print(user_id)
        print(type(user_id))
        users = data_users.read_json()
        roles = data_roles.read_json()
        print(users)
        role_id = users.get(user_id).get('role_id')
        role_id = str(role_id)
        action = callback.data.split('_')[0]
        all_points = roles.get(role_id).get(f'all_points_{action}')
        all_points = {int(k): v for k, v in all_points.items()}
        done_points = roles.get(role_id).get(f'done_points_{action}')
        if done_points:
            points = set(all_points) - set(done_points)
            text = 'Чек-лист уже выполняется'
            data_roles.write_file_json(roles)
        else:
            points = all_points
            text = 'Начните выполнение чеклиста, выбрав один из пунктов:'
        callback_messages = roles.get(role_id).get('callback_messages')
        callback_messages.append((message.message_id, message.chat.id))
        data_roles.write_file_json(roles)
        markup = types.InlineKeyboardMarkup(row_width=1)
        for point_id in points:
            btn = types.InlineKeyboardButton(
                text=f'{point_id}. {all_points[point_id]}',
                callback_data=f'{action}_point_{point_id}'
            )
            markup.add(btn)
        self.bot.edit_message_text(
            chat_id=message.chat.id,
            text=text,
            message_id=message.message_id,
            reply_markup=markup
        )

    def process_point(self, callback):
        message = callback.message
        user_id = str(message.chat.id)
        users = data_users.read_json()
        roles = data_roles.read_json()
        role_id = users.get(user_id).get('role_id')
        role_id = str(role_id)
        action = callback.data.split('_')[0]
        point_id = int(callback.data.split('_')[-1])
        all_points = roles.get(role_id).get(f'all_points_{action}')
        all_points = {int(k): v for k, v in all_points.items()}
        done_points = roles.get(role_id).get(f'done_points_{action}')
        if point_id in done_points:
            text = f'Пункт No{point_id} уже был выполнен!'
        else:
            done_points.append(point_id)

        points = set(all_points) - set(done_points)
        data_roles.write_file_json(roles)
        if points:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for btn_point_id in points:
                btn = types.InlineKeyboardButton(
                    text=f'{btn_point_id}. {all_points[btn_point_id]}',
                    callback_data=f'{action}_point_{btn_point_id}'
                )
                markup.add(btn)
                text = f'{point_id} - ok!'
        else:
            markup = main_markup
            for admin_user_id in users:
                if users.get(admin_user_id).get('role_id') == 777:
                    self.bot.send_message(
                        chat_id=admin_user_id,
                        text=f'Здравствуйте, {users.get(admin_user_id).get("first_name")}! Был выполнен чеклист ⬇ ',
                        reply_markup=markup
                    )
            roles[role_id]['done_points_open'] = []
            roles[role_id]['done_points_close'] = []
        text = f'Чеклист выполнен. Данные отправлены администраци'
        callback_messages = roles.get(role_id).get('callback_messages')
        for message in callback_messages:
            self.bot.edit_message_text(
                chat_id=message[1],
                text=text,
                message_id=message[0],
                reply_markup=markup
            )
        if not points:
            roles[role_id]['callback_messages'] = []
        data_roles.write_file_json(roles)

    def run(self):
        self.bot.infinity_polling()


if __name__ == '__main__':
    my_bot = MyPot()
    my_bot.run()


