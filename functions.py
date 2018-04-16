# -*- coding: utf-8 -*-
from telebot import types


def headline_wrapper(headline):
    """
    Формируем и возвращаем обработанный заголовок сообщения
    """
    return '<b>' + headline + '</b>\r\n\r\n'


def message_wrapper(message):
    """
    Формируем и возвращаем готовое сообщение
    """
    if "headline" in message:
        return headline_wrapper(str(message["headline"])) + str(message["text"])
    else:
        return message["text"]


def get_keyboard_inline_main():
    """
    Формируем и возвращаем основную встроенную клавиатуру
    """
    keyboard = types.InlineKeyboardMarkup()
    button_help = types.InlineKeyboardButton(text="Посмотреть список команд", callback_data="help")
    button_menu = types.InlineKeyboardButton(text="Перейти в меню", callback_data="menu")
    keyboard.row(button_help)
    keyboard.row(button_menu)
    return keyboard


def get_keyboard_inline_teachers():
    """
    Формируем и возвращаем основную встроенную клавиатуру с поиском преподавателя
    """
    keyboard = get_keyboard_inline_main()
    button_teachers = types.InlineKeyboardButton(text="Найти другого преподавателя", callback_data="teachers")
    keyboard.row(button_teachers)
    return keyboard


def get_keyboard_inline_departments():
    """
    Формируем и возвращаем основную встроенную клавиатуру с поиском преподавателя
    """
    keyboard = get_keyboard_inline_main()
    button_departments = types.InlineKeyboardButton(text="Найти другую кафедру", callback_data="departments")
    keyboard.row(button_departments)
    return keyboard


def get_keyboard_inline_subdivisions():
    """
    Формируем и возвращаем основную встроенную клавиатуру с поиском преподавателя
    """
    keyboard = get_keyboard_inline_main()
    button_departments = types.InlineKeyboardButton(text="Найти другое подразделение", callback_data="subdivisions")
    keyboard.row(button_departments)
    return keyboard