from requests import Response

from api.custom_request import MethodEnum
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresUnknown(ReqresIn):
    """ Класс эндпоинта /unknown/   """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/unknown'

    def get_unknown_list(self) -> Response:
        """ Получить список ресурсов """
        return self.request(method=MethodEnum.GET, url=self.url)

    def get_single_unknown(self, resource_id: int) -> Response:
        """Получить информацию о ресурсе

        Args:
            resource_id: идентификатор ресурса
        """
        return self.request(method=MethodEnum.GET, url=f'{self.url}/{resource_id}')
