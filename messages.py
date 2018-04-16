# -*- coding: utf-8 -*-
import config
from db import DataBase
from states import State
import functions as func
from telebot import types
import sqlite3


db = DataBase(config.db_path, config.db_file)

class Message:
    def __init__(self, bot, db_path):
        self.db_path = db_path
        self.bot = bot


    def get_start(self, message):
        """
        Обрабатываем и возвращаем стартовое сообщение
        """
        db.set_state(message.chat.id, State.START.value)

        self.bot.send_message(message.chat.id,
                         func.message_wrapper({
                             'headline': 'Начало работы',
                             'text': 'Нажмите /menu, чтобы выбрать подходящее действие.\n\rЕсли у Вас возникнут вопросы, введите команду /help'}),
                         reply_markup=func.get_keyboard_inline_main(),
                         parse_mode="HTML")


    def get_help(self, message):
        """
        Обрабатываем и возвращаем сообщение помощи (справки)
        """
        db.set_state(message.chat.id, State.HELP.value)

        # Добавляем встроенную клавиатуру с кнопкой меню
        keyboard = types.InlineKeyboardMarkup()
        button_menu = types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu")
        keyboard.add(button_menu)

        self.bot.send_message(message.chat.id,
                         func.message_wrapper({
                             'headline': 'Список доступных команд',
                             'text': '<b>Основные команды:</b>\r\n'
                                     '/start - стартовое сообщение\r\n'
                                     '/menu - главное меню\r\n'
                                     '/help - справка по работе с ботом.\r\n\r\n'
                                     '<b>Дополнительные команды:</b>\r\n'
                                     '/teacher - поиск преподавателя\r\n'
                                     '/department - поиск кафедры\r\n'
                                     '/subdivision - поиск подразделения.'}),
                         reply_markup=keyboard,
                         parse_mode="HTML")


    def get_menu(self, message):
        """
        Обрабатываем и возвращаем сообщение с основным меню
        """
        db.set_state(message.chat.id, State.MENU.value)

        # Добавляем клавиатуру с выбором пунктов меню
        markup = types.ReplyKeyboardMarkup()
        item_1 = types.KeyboardButton('🗓')
        item_2 = types.KeyboardButton('👩‍💼👨‍💼')
        item_3 = types.KeyboardButton('🚪')
        item_4 = types.KeyboardButton('🗄')
        item_5 = types.KeyboardButton('🍲🌮')
        item_6 = types.KeyboardButton('🖨📐')
        item_7 = types.KeyboardButton('📞')
        item_8 = types.KeyboardButton('📋')
        markup.row(item_1, item_2, item_3, item_4)
        markup.row(item_5, item_6, item_7, item_8)

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Главное меню',
                                  'text': '1. 🗓 посмотреть расписание @Schedule_MIET_bot;\r\n'
                                  '2. 👩‍💼👨‍💼 узнать информацию о преподавателе;\r\n'
                                  '3. 🚪 найти кафедру;\r\n'
                                  '4. 🗄 найти подразделение;\r\n'
                                  '5. 🍲🌮 найти столовую или буфет поблизости;\r\n'
                                  '6. 🖨📐 найти магазин канцтоваров или киоск, где можно распечатать документы;\r\n'
                                  '7. 📞 сообщить о проблеме или задать вопрос;\r\n'
                                  '8. 📋 справка по работе с ботом /help.\r\n\r\n'
                                  'Выберите подходящее действие:'
                              }),
                              reply_markup=markup,
                              parse_mode="HTML")


    def get_schedule(self, message, markup):
        """
        Возвращаем сообщение с информацией о расписании занятий
        """
        db.set_state(message.chat.id, State.SCHEDULE.value)

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Расписание занятий',
                                  'text': 'Вы можете узнать расписание занятий для своей группы двумя способами:'}),
                              reply_markup=markup,
                              parse_mode="HTML")

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'text': '1. воспользоваться сторонним ботом: @Schedule_MIET_bot\n\r'
                                          '2. посмотреть на сайте МИЭТа: http://miet.ru/schedule'
                              }),
                             reply_markup=func.get_keyboard_inline_main(),
                              parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_teacher_input(self, message, markup = None):
        """
        Возвращаем сообщение с просьбой о вводе данных преподавателя
        """
        db.set_state(message.chat.id, State.TEACHERS.value)

        if markup is not None:
            self.bot.send_message(message.chat.id,
                                  func.message_wrapper({
                                      'headline': 'Поиск преподавателя',
                                      'text': 'Введите фамилию, ФИ или ФИО преподавателя:'
                                  }),
                                  reply_markup=markup,
                                  parse_mode="HTML")
        else:
            self.bot.send_message(message.chat.id,
                                  func.message_wrapper({
                                      'headline': 'Поиск преподавателя',
                                      'text': 'Введите фамилию, ФИ или ФИО преподавателя:'
                                  }),
                                  parse_mode="HTML")


    def get_department_input(self, message, markup = None):
        """
        Возвращаем сообщение с просьбой о вводе аббревиатуры кафедры
        """
        db.set_state(message.chat.id, State.DEPARTMENTS.value)
        db_d = sqlite3.connect(self.db_path + 'departments.db')

        cursor = db_d.cursor()
        cursor.execute("SELECT * FROM departments")
        data = cursor.fetchall()

        # Формируем список доступных кафедр
        i = 1
        subdivisions = ''
        for row in data:
            subdivisions += str(i) + '. ' + row[1] + '\r\n'
            i += 1


        if markup is not None:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск кафедры',
                                      'text': 'В данный момент добавлены следующие кафедры МИЭТа:\r\n\r\n' + subdivisions + '\r\n'
                                                                                                                            'Введите аббревиатуру кафедры, которая указана выше (Например, ВМ-2):'
                                  }),
                                  reply_markup=markup,
                                  parse_mode="HTML")
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск кафедры',
                                      'text': 'В данный момент добавлены следующие кафедры МИЭТа:\r\n\r\n' + subdivisions + '\r\n'
                                                                                                                            'Введите аббревиатуру кафедры, которая указана выше (Например, ВМ-2):'
                                  }),
                                  parse_mode="HTML")



    def get_department(self, message, markup = None):
        """
        Проверяем и возвращаем информацию о кафедре института
        """
        db_d = sqlite3.connect(self.db_path + 'departments.db')

        cursor = db_d.cursor()
        department_name = [message.text.upper()]

        cursor.execute("SELECT * FROM departments WHERE cipher = ?", department_name)
        data = cursor.fetchone()

        if data is None:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск кафедры',
                                      'text': 'К сожалению, кафедры с таким названием нет в базе данных!'
                                  }),
                                  reply_markup=func.get_keyboard_inline_departments(),
                                  parse_mode="HTML")
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'text': '<b>Кафедра:</b> ' + data[1] + '\r\n'
                                      '<b>Аудитория:</b> ' + data[5] + '\r\n'
                                      '<b>Телефон:</b> ' + data[3] + '\r\n'
                                      '<b>E-mail:</b> ' + data[6] + '\r\n'
                                      '<b>Подробнее:</b> ' + data[7] + '\r\n'
                                  }),
                                  reply_markup=func.get_keyboard_inline_departments(),
                                  parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_subdivision_input(self, message, markup = None):
        """
        Возвращаем сообщение с просьбой о вводе аббревиатуры подразделения
        """
        db.set_state(message.chat.id, State.SUBDIVISION.value)
        db_s = sqlite3.connect(self.db_path + 'subdivisions.db')

        cursor = db_s.cursor()
        cursor.execute("SELECT * FROM subdivisions")
        data = cursor.fetchall()

        # Формируем список доступных подразделений
        i = 1
        subdivisions = ''
        for row in data:
            subdivisions += str(i) + '. ' + row[1] + '\r\n'
            i += 1


        if markup is not None:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск подразделений',
                                      'text': 'В данный момент добавлены следующие подразделения МИЭТа:\r\n\r\n' + subdivisions + '\r\n'
                                                                                                                                  'Введите аббревиатуру подразделения, которая указана выше (Например, ДОСУП):'
                                  }),
                                  reply_markup=markup,
                                  parse_mode="HTML")
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск подразделений',
                                      'text': 'В данный момент добавлены следующие подразделения МИЭТа:\r\n\r\n' + subdivisions + '\r\n'
                                                                                                                                  'Введите аббревиатуру подразделения, которая указана выше (Например, ДОСУП):'
                                  }),
                                  parse_mode="HTML")


    def get_subdivision(self, message):
        """
        Проверяем и возвращаем информацию о подразделении института
        """
        db_s = sqlite3.connect(self.db_path + 'subdivisions.db')

        cursor = db_s.cursor()
        subdivision_name = [message.text.upper()]

        cursor.execute("SELECT * FROM subdivisions WHERE cipher = ?", subdivision_name)
        data = cursor.fetchone()

        if data is None:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск подразделения',
                                      'text': 'К сожалению, подразделений с таким названием нет в базе данных!'
                                  }),
                                  reply_markup=func.get_keyboard_inline_subdivisions(),
                                  parse_mode="HTML")
        else:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск подразделения',
                                      'text': '<b>Подразделение:</b> ' + data[1] + '\r\n'
                                              '<b>Руководитель:</b> ' + data[3] + '\r\n'
                                              '<b>Аудитория:</b> ' + data[5] + '\r\n'
                                              '<b>Телефон:</b> ' + data[4] + '\r\n'
                                              '<b>Email:</b> ' + data[6] + '\r\n'
                                              '<b>Подробнее:</b> ' + data[7]
                                  }),
                                  reply_markup=func.get_keyboard_inline_subdivisions(),
                                  parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_buffet_input(self, message, markup):
        """
        Возвращаем сообщение с просьбой о вводе корпуса, в котором он сейчас находится
        """
        db.set_state(message.chat.id, State.BUFFETS.value)

        self.bot.send_photo(message.chat.id,
                            open('images/other/miet.jpg', 'rb'),
                            caption="Схема расположения корпусов «МИЭТ»",
                            reply_markup=markup)

        # Добавляем основную клавиатуру
        markup = types.ReplyKeyboardMarkup()
        item_1 = types.KeyboardButton('1')
        item_2 = types.KeyboardButton('2')
        item_3 = types.KeyboardButton('3')
        item_4 = types.KeyboardButton('4')
        item_5 = types.KeyboardButton('5')
        markup.row(item_1, item_2, item_3, item_4, item_5)

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Поиск столовой или буфета',
                                  'text': 'Выберите номер корпуса, в котором Вы находитесь сейчас или поблизости:'}),
                              reply_markup=markup,
                              parse_mode="HTML")


    def get_first_buffet(self, message):
        """
        Возвращает первый слайд галереи
        """
        row = db.get_buffets(int(message.text), 1)
        next_button_text = message.text + "_2"

        markup = types.ReplyKeyboardRemove()
        keyboard = types.InlineKeyboardMarkup()
        button_menu = types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu")
        button_next = types.InlineKeyboardButton(text=">", callback_data=next_button_text)
        keyboard.add(button_menu, button_next)

        current_photo = 'images/buffets/' + str(row[2]) + '.jpg'
        self.bot.send_photo(message.chat.id,
                            open(current_photo, 'rb'),
                            reply_markup=markup,
                            caption=row[4])

        self.bot.send_message(chat_id=message.chat.id,
                              text=func.message_wrapper({
                              'text': '<b>Местоположение:</b> ' + row[4] + '.\r\n'
                                      '<b>График работы:</b> ' + row[5] + '.'
                              }),
                              reply_markup=keyboard,
                              parse_mode="HTML")

        db.set_state(message.chat.id, State.BUFFETS_GALLERY.value)


    def get_store_input(self, message, markup):
        """
        Возвращаем магазины канцтоваров
        """
        db.set_state(message.chat.id, State.STORES.value)

        self.bot.send_photo(message.chat.id,
                            open('images/other/miet.jpg', 'rb'),
                            caption="Схема расположения корпусов «МИЭТ»",
                            reply_markup=markup)

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Магазины канцтоваров',
                                  'text': 'На данный момент действует только один магазин канцторваров, в котором Вы также можете распечатать нужные документы!'}),
                              reply_markup=markup,
                              parse_mode="HTML")

        self.bot.send_photo(message.chat.id,
                            open("images/stores/1.jpg", "rb"),
                            caption="На фотографии представлен магазин канцелярских товаров")

        self.bot.send_message(message.chat.id,
                              text=func.message_wrapper({
                                  'text': '<b>Местоположение:</b> 3 корпус, 2 этаж, около главной лестницы\r\n'
                                          '<b>Возможности:</b> можно приобрести канцелярские товары или распечатать документы\r\n'
                                          '<b>Время работы:</b> пн. — пт.: 10:00 — 15:00'
                              }),
                              reply_markup=func.get_keyboard_inline_main(),
                              parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_feedback(self, message, markup):
        """
        Возвращаем информацию об обратной связи
        """
        db.set_state(message.chat.id, State.FEEDBACK.value)

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Обратная связь',
                                  'text': 'Вы можете сообщить нам о возникшей у Вас проблеме или задать вопрос касательно работы этого бота!'}),
                              reply_markup=markup,
                              parse_mode="HTML")

        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'text': 'Для этого воспользуйтесь другим нашим ботом: @mietINFO_feedback_bot'}),
                              reply_markup=func.get_keyboard_inline_main(),
                              parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_choice_error(self, message):
        """
        Возвращаем ошибку выбора, если пользователь не нажал на кнопку
        """
        self.bot.send_message(message.chat.id,
                              func.message_wrapper({
                                  'headline': 'Выбор действия',
                                  'text': 'Вы не выбрали ни одного из предложенных действий!\r\n'
                                          'Нажмите на одну из предложенных кнопок:'}),
                              parse_mode="HTML")


    def get_teacher(self, message):
        db_t = sqlite3.connect(self.db_path + 'teachers.db')
        cursor = db_t.cursor()

        teacher_name = message.text.lower().title()
        cursor.execute("SELECT * FROM teachers WHERE name LIKE ?", ('%{}%'.format(teacher_name),))
        data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM teachers WHERE name LIKE ?", ('%{}%'.format(teacher_name),))
        count = cursor.fetchone()

        i = 0
        for row in data:
            name = row[1] if row[1] is not None else 'не указано'
            department = row[2] if row[2] is not None else 'не указано'
            occupation = row[3] if row[3] is not None else 'не указана'
            place = row[4] if row[4] is not None else 'не указана'
            phone = row[5] if row[5] is not None else 'не указан'
            mail = row[6] if row[6] is not None else 'не указан'
            link = row[7] if row[7] is not None else 'не указано'
            photo = row[8]


            if photo is not None or requests.head(photo) == 200:
                self.bot.send_photo(chat_id=message.chat.id,
                                photo=photo)

            self.bot.send_message(chat_id=message.chat.id,
                              text=func.message_wrapper({
                                  'text': '<b>ФИО:</b> ' + name + '\r\n'
                                          '<b>Подразделение:</b> ' + department + '\r\n'
                                          '<b>Должность:</b> ' + occupation + '\r\n'
                                          '<b>Аудитория:</b> ' + place + '\r\n'
                                          '<b>Телефон:</b> ' + phone + '\r\n'
                                          '<b>E-mail:</b> ' + mail + '\r\n'
                                          '<b>Подробнее:</b> ' + link
                              }),
                              reply_markup=func.get_keyboard_inline_teachers() if i == (count[0] - 1) else False,
                              parse_mode="HTML")

            i += 1


        if count[0] == 0:
            self.bot.send_message(chat_id=message.chat.id,
                                  text=func.message_wrapper({
                                      'headline': 'Поиск преподавателя',
                                      'text': 'К сожалению, преподавателя с такими инициалами нет в базе данных!'
                                  }),
                                  reply_markup=func.get_keyboard_inline_teachers(),
                                  parse_mode="HTML")

        db.set_state(message.chat.id, State.FINISH.value)


    def get_buffets_gallery(self, call):
        """
        Возвращаем новый слайд галереи или меню выбора
        """
        if call.data == "menu":
            self.get_menu(call.message)
        else:
            self.bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id - 1)

            self.bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)

            key = call.data.split("_")
            prev_button_text = key[0] + "_" + str(int(key[1]) - 1)
            next_button_text = key[0] + "_" + str(int(key[1]) + 1)

            row = db.get_buffets(int(key[0]), int(key[1]))

            markup = types.ReplyKeyboardRemove()
            keyboard = types.InlineKeyboardMarkup()
            if prev_button_text:
                button_prev = types.InlineKeyboardButton(text="<", callback_data=prev_button_text)

            if next_button_text:
                button_next = types.InlineKeyboardButton(text=">", callback_data=next_button_text)

            button_menu = types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu")

            if int(key[1]) > 1 and int(key[1]) < (db.get_buffets_count(int(key[0]))[0] - 1):
                keyboard.add(button_prev, button_menu, button_next)
            elif int(key[1]) == 1:
                keyboard.add(button_menu, button_next)
            elif int(key[1]) == (db.get_buffets_count(int(key[0]))[0] - 1):
                keyboard.add(button_prev, button_menu)
            else:
                keyboard.add(button_menu)

            current_photo = 'images/buffets/' + str(row[2]) + '.jpg'
            self.bot.send_photo(call.message.chat.id,
                           open(current_photo, 'rb'),
                           reply_markup=markup,
                           caption=row[3])

            self.bot.send_message(chat_id=call.message.chat.id,
                             text=func.message_wrapper({
                                 'text': '<b>Местоположение:</b> ' + row[4] + '\r\n'
                                         '<b>График работы:</b> ' + row[5] + ''
                             }),
                             reply_markup=keyboard,
                             parse_mode="HTML")