from random import choice

places = ['Макдоли', "КФС", "Бургера Кинга", "ТАКОС НАХУЙ", "ЧИКАН", "ХУЙЛАН", "КАПИТАН"]


def pick():
    """Return random fast food place"""
    return choice(places)