from typing import Optional

from requests import Response

from api.frame_request import MethodEnum
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresUsers(ReqresIn):
    """ Класс эндпоинта /users/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/users'

    def get_users(self, params: dict[str, str]) -> Response:
        """ Получить информацию о пользователях

        Args:
            params: Параметры запроса:
                page - номер страницы
                delay - таймаут ожидания перед получением тела
        """
        return self.request(method=MethodEnum.GET, url=self.url, params=params)

    def get_single_user(self, user_id: int) -> Response:
        """ Получить информацию о пользователе

        Args:
            user_id: идентификатор пользователя
        """
        return self.request(method=MethodEnum.GET, url=f'{self.url}/{user_id}')

    def create_user(self, data: Optional[str] = None, json: Optional[dict] = None) -> Response:
        """Создать пользователя

        Args:
            data: тело запроса в формате str
                name - имя пользователя
                job - должность
            json: тело запроса в формате dict
        """
        return self.request(method=MethodEnum.POST, url=self.url, data=data, json=json)

    def update_user(self, method: MethodEnum, user_id: int, data: Optional[str] = None, json: Optional[dict] = None):
        """Обновить пользователя

        Args:
            method: PUT или PATCH
            user_id: идентификатор пользователя
            data: тело запроса в формате str
                name - имя пользователя
                job - должность
            json: тело запроса в формате dict
        """
        return self.request(method=method, url=f'{self.url}/{user_id}', data=data, json=json)

    def delete_user(self, user_id: int):
        """Удалить пользователя

        Args:
            user_id: идентификатор пользователя
        """
        return self.request(method=MethodEnum.DELETE, url=f'{self.url}/{user_id}')
