"""Методы валидации тел ответа по схеме Pydantic"""
from json import dumps
from typing import Type, TypeVar, Generic

from allure import attach, step
from pydantic import BaseModel, ValidationError
from pytest import fail

from other.logging import logger

Model = TypeVar('Model', bound=BaseModel)


class GenericModelList(Generic[Model], BaseModel):
    """Универсальный класс дженерик с корневым типом список

    Examples:
        my_list_model = GenericModelList[MyModel].model_validate(my_list) - преобразование в модель списка словарей
        my_list_model = GenericModelList[MyModel].model_validate_json(my_json) - преобразование в модель строки формата json
        model.is_valid(GenericModelList[MyModel], DATA) - валидация списка словарей на соответствие модели

    """
    __root__: list[Model]


@logger.catch
@step('Валидация тела ответа по схеме')
def is_valid(model: Type[BaseModel], response: dict):
    """Валидировать тело ответа по схеме

    Args:
        model: Схема тела ответа
        response: JSON, dict, list ответа
    """
    with step('Проверка тела по схеме'):
        _model, _response = model.model_json_schema(), dumps(response)
        attach(_response, name='Тело ответа')
        attach(str(_model), name='Модель')

        try:
            model.model_validate(response)

        except ValidationError as e:
            logger.error(
                f'Ошибка валидации тела ответа!'
                f'\nОшибка:\n{e}\n'
                f'\nМодель: {_model}'
                f'\nТело:   {_response}'
            )
            fail(reason=str(e))
