# -*- coding: utf-8 -*-
from enum import Enum

class State(Enum):
    """
    Состояния бота
    """
    START = 1
    HELP = 2
    MENU = 3
    SCHEDULE = 4
    TEACHERS = 5
    DEPARTMENTS = 6
    SUBDIVISION = 7
    BUFFETS = 8
    BUFFETS_GALLERY = 9
    STORES = 10
    FEEDBACK = 11
    FINISH = 12