from typing import Optional

from requests import Response

from api.custom_request import MethodEnum
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresLogin(ReqresIn):
    """ Класс эндпоинта /login/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/login'

    def post_login(self, data: Optional[str] = None, json: Optional[dict] = None) -> Response:
        """ Отправить запрос на авторизацию

        Args:
            data: тело запроса
                email - почта пользователя
                password - пароль пользователя
            json: тело запроса
        """
        return self.request(method=MethodEnum.POST, url=self.url, data=data, json=json)
