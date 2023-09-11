from enum import Enum
from typing import Optional, Union

import requests
from requests import Response, request

from other.logging import log_request, log_response


class MethodEnum(Enum):
    """ Перечисление доступных методов запроса"""
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Request:
    """Класс для отправки API-запросов"""
    headers, params, data, files, json, token_cache = {}, {}, {}, {}, {}, {}

    def request(
            self,
            url: str,
            method: MethodEnum,
            headers: Optional[dict[str, str]] = None,
            data: Optional[Union[dict, list, str]] = None,
            params: Optional[dict[str, str]] = None,
            timeout: Optional[Union[int, float]] = None,
            json: Optional[dict] = None
    ) -> Response:
        """Отправить запрос и залогировать запрос и ответ

        Args:
            url: адрес
            method: HTTP-метод
            headers: заголовки, если есть
            data: тело запроса, если есть
            json: тело запроса в формате dict
            params: параметры запроса, если есть
            timeout: таймаут, который надо выждать прежде чем отправить запрос
        """
        log_request(
            request=requests.Request(
                url=url,
                method=method.value,
                headers=headers if headers else self.headers,
                params=params if params else self.params,
                data=data if data else self.data,
                json=json if json else self.json
            ).prepare()
        )

        response = request(
            url=url,
            method=method.value,
            headers=headers if headers else self.headers,
            params=params if params else self.params,
            data=data if data else self.data,
            json=json if json else self.json,
            verify=False,
            timeout=timeout
        )
        log_response(response=response)

        return response
