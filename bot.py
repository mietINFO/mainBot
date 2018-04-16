# -*- coding: utf-8 -*-
import db
import telebot
import messages
import cherrypy
from telebot import types
from states import State
import config


# Настройки вебхуков
WEBHOOK_HOST = '<your_host>'
WEBHOOK_PORT = 88  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

# Путь к сертификатам
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

# Путь к боту
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)
msg = messages.Message(bot, config.db_path)
db = db.DataBase(config.db_path, config.db_file)

# Вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)



@bot.message_handler(commands=['start'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_start_message(message):
    """
    Выводим стартовое сообщение
    """
    msg.get_start(message)


@bot.message_handler(commands=['help'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_help_message(message):
    """
    Выводим справку для пользователя
    """
    msg.get_help(message)


@bot.message_handler(commands=['menu'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_menu_message(message):
    """
    Выводим меню выбора
    """
    msg.get_menu(message)


@bot.message_handler(commands=['teacher'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_teacher_message(message):
    """
    Выводим запрос преподавателя
    """
    msg.get_teacher_input(message)


@bot.message_handler(commands=['department'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_department_message(message):
    """
    Выводим запрос кафедры
    """
    msg.get_department_input(message)


@bot.message_handler(commands=['subdivision'], func=lambda message: db.get_state(message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def get_subdivision_message(message):
    """
    Выводим запрос подразделения
    """
    msg.get_subdivision_input(message)


@bot.callback_query_handler(func=lambda call: db.get_state(call.message.chat.id) in [State.START.value, State.HELP.value, State.MENU.value, State.FINISH.value])
def callback_inline(call):
    """
    Выводим сообщение, которое вызвано из встроенной клавиатуры
    """
    if call.data == "menu":
        msg.get_menu(call.message)
    elif call.data == "help":
        msg.get_help(call.message)
    elif call.data == "teachers":
        msg.get_teacher_input(call.message)
    elif call.data == "departments":
        msg.get_department_input(call.message)
    elif call.data == "subdivisions":
        msg.get_subdivision_input(call.message)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) in [State.MENU.value, State.HELP.value, State.FINISH.value], content_types=['text'])
def get_choice_menu_message(message):
    """
    Выводим определённое действие меню
    """
    markup = types.ReplyKeyboardRemove(selective=False)

    if message.text == '🗓':
        msg.get_schedule(message, markup)
    elif message.text == '👩‍💼👨‍💼':
        msg.get_teacher_input(message, markup)
    elif message.text == '🚪':
        msg.get_department_input(message, markup)
    elif message.text == '🗄':
        msg.get_subdivision_input(message, markup)
    elif message.text == '🍲🌮':
        msg.get_buffet_input(message, markup)
    elif message.text == '🖨📐':
        msg.get_store_input(message, markup)
    elif message.text == '📞':
        msg.get_feedback(message, markup)
    elif message.text == '📋':
        msg.get_help(message)
    else:
        msg.get_choice_error(message)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == State.TEACHERS.value)
def get_teacher_message(message):
    """
    Выводим определённого преподавателя
    """
    msg.get_teacher(message)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == State.DEPARTMENTS.value)
def get_department_message(message):
    """
    Выводим определённую кафедру
    """
    msg.get_department(message)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == State.SUBDIVISION.value)
def get_subdivision_message(message):
    """
    Выводим определённое подразделение
    """
    msg.get_subdivision(message)


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) == State.BUFFETS.value)
def get_buffets_message(message):
    """
    Выводим первый слайд галереи
    """
    if message.text in ["1", "2", "3", "4", "5"]:
        msg.get_first_buffet(message)


@bot.callback_query_handler(func=lambda call: db.get_state(call.message.chat.id) == State.BUFFETS_GALLERY.value)
def callback_buffets(call):
    """
    Выводим один из слайдов галереи
    """
    msg.get_buffets_gallery(call)



# Снимаем вебхук перед повторной установкой
bot.remove_webhook()

# Ставим вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

 # Запуск вебхук-сервера
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})