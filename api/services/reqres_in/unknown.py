from api.custom_request import MethodEnum
from api.custom_response import CustomResponse
from api.services.reqres_in.reqres_in import ReqresIn


class ReqresUnknown(ReqresIn):
    """ Класс эндпоинта /unknown/   """

    def __init__(self):
        super().__init__()
        self.url = f'{self.url}/unknown'

    def get_unknown_list(self) -> CustomResponse:
        """ Получить список ресурсов """
        return self.request(method=MethodEnum.GET, url=self.url)

    def get_single_unknown(self, resource_id: int) -> CustomResponse:
        """Получить информацию о ресурсе

        Args:
            resource_id: идентификатор ресурса
        """
        return self.request(method=MethodEnum.GET, url=f'{self.url}/{resource_id}')
