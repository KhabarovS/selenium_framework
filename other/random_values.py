from datetime import date, datetime, timedelta
from random import randint
from string import ascii_lowercase, digits

from allure import step
from mimesis.random import Random

from other.logging import logger

msg = 'ГЕНЕРАТОР {gen}.\nРЕЗУЛЬТАТ: {result}'


@step('Генератор. Получить случайное число')
def get_random_number(start: int = 1, end: int = 999999, length: int = None) -> int:
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
def get_random_string():
    """ Получить случайную строку """
    result = Random()._generate_string(str_seq=f'абвгдеёжзийклмнопрстуфхцчшщьыъэюя{ascii_lowercase}{digits}')
    logger.info(msg.format(gen='cлучайной строки', result=result))

    return result


@step('Генератор. Получить текущую дату и/или время в формате')
def get_current_datetime(fmt: str = "%d.%m.%YT%H:%M:%S") -> str:
    """Получить текущую дату

    Args:
        fmt: формат даты
    """
    result = datetime.now().strftime(fmt)
    logger.info(msg.format(gen='текущей даты', result=result))

    return result


@step('Генератор. Получить дату и/или время со смещением')
def get_datetime_with_offset(fmt: str = "%d.%m.%YT%H:%M:%S", to_the_future: bool = True, utc: bool = False,
                             working_day: bool = False, holiday: bool = False, seconds: int = 0, minutes: int = 0,
                             hours: int = 0, days: int = 0, weeks: int = 0) -> str:
    """ Получить текущую дату со сдвигом

    Args:
        fmt:            формат времени. Например "%Y-%m-%dT%H:%M:%S+03:00"
        to_the_future:  флаг указывающий сдвиг в будущее
        working_day:    смещать дату на рабочий день
        holiday:        смещать дату на выходной день
        seconds:        количество секунд сдвига
        minutes:        количество минут сдвига
        hours:          количество часов сдвига
        days:           количество дней сдвига
        weeks:          количество недель сдвига
        utc:            флаг необходимости использования часового пояса UTC
    """
    date_with_offset = datetime.utcnow() if utc else datetime.today()
    delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
    date_with_offset = date_with_offset + delta if to_the_future else date_with_offset - delta

    if working_day:
        number_of_day = date.isoweekday(date_with_offset)

        if number_of_day in (6, 7):
            date_with_offset += timedelta(days=(8 - number_of_day))

    if holiday:
        date_with_offset += timedelta(days=(6 - date.isoweekday(date_with_offset)))

    result = date_with_offset.strftime(fmt)
    logger.info(msg.format(gen='даты со смещением', result=result))

    return result
