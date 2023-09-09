from json import dumps

from allure import attach, attachment_type, step
from jsonpath_rw_ext import parse
from requests import PreparedRequest

from other.logging import logger


@logger.catch
def get_curl(request: PreparedRequest, is_compressed: bool = False, is_insecure: bool = False):
    """Получить curl запроса

    Args:
        request: запрос
        is_compressed: параметр позволяющий сформировать curl для запроса сжатого ответа
        is_insecure: параметр явно позволяет сформировать curl для "небезопасного" SSL соединения и передачи данных
    """
    headers = ' -H '.join([f'"{k}: {v}"' for k, v in request.headers.items()])
    return f"curl -X {request.method} -H {headers} " \
           f"-d '{request.body.decode('latin-1') if isinstance(request.body, bytes) else request.body}' " \
           f"{'--compressed' if is_compressed else ''} " \
           f"{'--insecure' if is_insecure else ''} '{request.url}"


@step('Поиск значения в словаре')
def find_value_from_json(json: dict, jp_expr: str) -> str or dict or list or bool or int:
    """ Найти значение в json по JPExpression

    Args:
        json: json, в котором надо найти значение
        jp_expr: путь до значения
    """
    found = [match.value for match in parse(jp_expr).find(json)]

    if len(found) > 1:
        result = found

    elif len(found) == 1:
        result = found[0]

    else:
        raise ValueError(f'Значение по пути {jp_expr} не найдено')

    attach(body=str(result), name='РЕЗУЛЬТАТ', attachment_type=attachment_type.TEXT)
    logger.info(
        f'Поиск значения из JSON\n'
        f'\tПуть:\t\t{jp_expr}\n'
        f'\tJSON:\t\t{dumps(json)}\n'
        f'\tЗначение:\t{result}\n'
        f'\tТип:\t\t{type(result)}'
    )
    return result
