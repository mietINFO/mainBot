# -*- coding: utf-8 -*-
import sqlite3


class DataBase:
    def __init__(self, db_path, db_file):
        self.db_file = db_path + db_file
        self.db = None


    def create_db(self):
        """
        Создание необходимых таблиц для работы с ботом
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()

        # Создаём таблицу users, если она не существует
        cursor.execute("""CREATE TABLE IF NOT EXISTS users
                      (
                        user_id INT PRIMARY KEY,
                        state INT
                      )""")

        self.db.commit()


        # Запрос к таблице buffets
        try:
            cursor.execute("""SELECT * FROM buffets LIMIT 1""")
        except sqlite3.Error:
            self.create_buffets_table()
            self.db.commit()


    def create_buffets_table(self):
        """
        Создаём таблицу с буфетами и столовыми
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()

        # Создаём таблицу buffets, если она не существует
        cursor.execute("""CREATE TABLE IF NOT EXISTS buffets
                                      (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        housing INT,
                                        photo INT,
                                        name TEXT,
                                        place TEXT,
                                        work_time TEXT
                                      )""")

        # Добавляем записи буфетов и столовых
        cursor.executescript("""
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (2, 6, "На фотографии представлена столовая", "2 корпус, 2 этаж, недалеко от перехода между 1 и 2 корпусом", "пн. — пт.: 09:00 — 15:00, сб.: 09:00 — 14:00");
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (1, 5, "На фотографии представлен буфет", "1 корпус, 1 этаж, недалеко от перехода между 1 и 3 корпусом", "пн. — пт.: 10:00 — 14:00");
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (3, 4, "На фотографии представлена столовая", "3 корпус, 1 этаж, недалеко от главной лестницы", "пн. — пт.: 09:00 — 15:00, сб.: 10:00 — 13:00");
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (3, 3, "На фотографии представлены два буфета", "3 корпус, 1 этаж, недалеко от перехода между 1 и 3 корпусом", "пн. — пт.: 10:00 — 16:00");
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (3, 2, "На фотографии представлены буфет", "3 корпус, 1 этаж, недалеко от перехода между 1 и 3 корпусом", "пн. — пт.: 10:00 — 14:00");
              INSERT INTO buffets (housing, photo, name, place, work_time) VALUES (4, 1, "На фотографии представлена пельменная", "4 корпус, 1 этаж", "пн. — пт.: 10:00 — 15:00");
              """)

        self.db.commit()


    def get_buffets(self, housing, number):
        """
        Возвращаем текущий буфет или столовую
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()
        number = number - 1

        if housing == 2:
            order = "housing ASC"
            housings = "2, 3, 4"
        elif housing == 3:
            order = "housing DESC"
            housings = "3, 2, 1"
        elif housing == 4:
            order = "housing DESC"
            housings = "4, 2, 1"
        else:
            order = "housing ASC"
            housings = "1, 3, 2"


        limit = str(number + 1) + ", " + str(number) if number else "0, 1"
        cursor.execute('SELECT * FROM buffets WHERE housing IN ({0}) ORDER BY {1} LIMIT {2}'.format(housings, order, limit))
        return cursor.fetchone()


    def get_buffets_count(self, housing):
        """
        Возвращает количество буфетов для определённого корпуса
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()


        if housing == 2:
            order = "housing ASC"
            housings = "2, 3, 4"
        elif housing == 3:
            order = "housing DESC"
            housings = "3, 2, 1"
        elif housing == 4:
            order = "housing DESC"
            housings = "4, 2, 1"
        else:
            order = "housing ASC"
            housings = "1, 3, 2"

        cursor.execute('SELECT COUNT(*) FROM buffets WHERE housing IN ({0}) ORDER BY {1}'.format(housings, order))
        return cursor.fetchone()


    def check_user(self, user_id):
        """
        Проверяем на существование пользователя в системе
        """
        self.create_db()

        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', [user_id])
        user = cursor.fetchone()

        if user == None:
            self.add_user(user_id)


    def add_user(self, user_id):
        """
        Добавляем нового пользователя в БД
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()

        data = [user_id, '1']
        cursor.execute('INSERT INTO users (user_id, state) VALUES (?, ?)', data)
        self.db.commit()


    def get_user(self, user_id):
        """
        Возвращаем данные определённого пользователя
        """
        self.db = sqlite3.connect(self.db_file)

        cursor = self.db.cursor()
        cursor.execute('SELECT state FROM users WHERE user_id = ?', [user_id])
        return cursor.fetchone()


    def get_state(self, user_id):
        """
        Возвращаем текущее состояние пользователя
        """
        self.check_user(user_id)
        return self.get_user(user_id)[0]


    def set_state(self, user_id, state):
        """
        Устанавливаем определённое состояние пользователя
        """
        self.db = sqlite3.connect(self.db_file)
        cursor = self.db.cursor()
        state = int(state)

        data = [state, user_id]
        cursor.execute('UPDATE users SET state = ? WHERE user_id = ?', data)
        self.db.commit()