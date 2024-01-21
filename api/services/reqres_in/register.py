from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresRegister(ReqresIn):
    """ Класс эндпоинта /register/ """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/register'

    def post_register(self, data: str | None = None, json: dict | None = None) -> CustomResponse:
        """ Отправить запрос на регистрацию

        Args:
            data: тело запроса
                email - почта пользователя
                password - пароль пользователя
            json: тело запроса
        """
        return self.request(method=MethodEnum.POST, url=self.url, data=data, json=json)
