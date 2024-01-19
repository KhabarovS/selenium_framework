from datetime import date, datetime, timedelta
from random import randint
from string import ascii_lowercase, digits
from typing import Optional

from allure import step
from mimesis.random import Random

from other.logging import logger

msg = 'ГЕНЕРАТОР {gen}.\nРЕЗУЛЬТАТ: {result}'


@step('Генератор. Получить случайное число')
def get_random_number(start: int = 1, end: int = 999999, length: Optional[int] = None) -> int:
    """ Получить случайное число в заданном диапазоне или заданной длины

    Args:
        start: начало диапазона;
        end: конец диапазона;
        length: длина числа.
    """
    result = randint(10 ** (length - 1), (10 ** length) - 1) if length else randint(start, end)
    logger.info(msg.format(gen='случайного числа', result=result))

    return result


@step('Генератор. Получить случайную строку')
def get_random_string(length: int):
    """ Получить случайную строку

    Args:
        length: длина строки
    """
    result = Random()._generate_string(
        str_seq=f'абвгдеёжзийклмнопрстуфхцчшщьыъэюя{ascii_lowercase}{digits}',
        length=length
    )
    logger.info(msg.format(gen='cлучайной строки', result=result))

    return result
