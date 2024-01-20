from typing import Optional

from requests import Response

from api.custom_request import MethodEnum
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresRegister(ReqresIn):
    """ Класс эндпоинта /register/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/register'

    def post_register(self, data: Optional[str] = None, json: Optional[dict] = None) -> Response:
        """ Отправить запрос на регистрацию

        Args:
            data: тело запроса
                email - почта пользователя
                password - пароль пользователя
            json: тело запроса
        """
        return self.request(method=MethodEnum.POST, url=self.url, data=data, json=json)
