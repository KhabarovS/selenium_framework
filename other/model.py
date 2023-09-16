"""Методы валидации тел ответа по схеме Pydantic"""
import json
from typing import Type

from allure import attach, step
from pydantic import BaseModel, ValidationError
from pytest import fail

from other.logging import logger


@logger.catch
@step('Валидация тела ответа по схеме')
def is_valid(model: Type[BaseModel], response: dict) -> bool:
    """Валидировать тело ответа по схеме

    Args:
        model: Схема тела ответа
        response: JSON, dict, list ответа
    """
    with step('Проверка тела по схеме'):
        _model, _response = model.model_json_schema(), json.dumps(response)
        attach(_response, name='Тело ответа')
        attach(str(_model), name='Модель')

        try:
            model.model_validate(response)

            return True

        except ValidationError as e:
            logger.error(
                f'Ошибка валидации тела ответа!'
                f'\nОшибка:\n{e}\n'
                f'\nМодель: {_model}'
                f'\nТело:   {_response}'
            )
            fail(reason=str(e))
