from typing import Type, Any

from allure import step
from pydantic import BaseModel
from requests import Response

from other import model

ERROR_STATUS_CUSTOM_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: {exp}'


class CustomResponse:
    """Кастомный объект ответа"""

    __slots__ = ['__response', 'request_model', 'response_model', '_response_body']

    def __init__(
            self,
            response: Response,
            request_model: Type[BaseModel] | None = None,
            response_model: Type[BaseModel] | None = None,
    ):
        self._response_body: dict[str, Any] | None = None
        self.__response = response
        self.request_model = request_model
        self.response_model = response_model

    @property
    def status_code(self) -> int:
        """Получить статус код ответа"""
        return self.__response.status_code

    @property
    def content(self) -> bytes:
        """Получить тело ответа в байт-строке"""
        return self.__response.content

    @property
    def text(self) -> str:
        """Вернуть тело в юникод строке"""
        return self.__response.text

    @property
    def links(self) -> dict[str, Any]:
        """Получить хедеры ответа в виде словаря"""
        return self.__response.links

    @step('Вызвать исключение при неуспешном статус коде(4xx, 5xx)')
    def raise_for_status(self):
        self.__response.raise_for_status()

    @step('Получить тело ответа в виде словаря или списка')
    def json(self, **kwargs) -> dict[str, Any] | list[dict[str, Any]]:
        """Получить ответ как словарь или список

        Args:
            **kwargs: кварги для преобразования .json()
        """
        if not hasattr(self, '__response_body'):
            self._response_body = self.__response.json(**kwargs) if self.content and len(self.content) > 0 else None

        return self._response_body

    @step('Преобразовать ответ в dto')
    def dto(self, **kwargs) -> BaseModel:
        """Получить ответ как data transfer object

        Args:
            **kwargs: кварги для преобразования .json()
        """
        if not self.response_model:
            raise AttributeError('Модель не задана')

        body = self._response_body if self._response_body else self.json(**kwargs)

        if body is None:
            raise ValueError('Невозможно преобразовать ответ в модель! Отсутствует тело ответа')

        return self.response_model(**body)

    @step('Проверить статус код')
    def check_expected_status_code(self, expected_code: int, exception: Type[Exception] | None = None):
        """Проверить статус код

        Args:
            expected_code: ожидаемый статус код
            exception: вызов исключения, вместо ассерта
        """
        msg = ERROR_STATUS_CUSTOM_MSG.format(code=self.status_code, exp=expected_code)

        if exception and self.status_code != expected_code:
            raise exception(msg)

        assert self.status_code == expected_code, msg

    @step('Валидировать ответ по схеме')
    def check_is_valid(self):
        """ Валидировать ответ по схеме"""
        model.is_valid(model=self.response_model, response=self.json())
