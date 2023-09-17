from allure import feature, title

from api.services.reqres_in.unknown import ReqresUnknown
from dto.unknown_dto import ResourceListResponseDto
from other import model
from tests.allure_constants import AllureApiResource


@feature('Проверить метод получения списка ресурсов GET /api/unknown')
class TestGetResourceList(AllureApiResource):

    @title('Получить список ресурсов с валидными параметрами')
    def test_get_resource_list(self):
        (response := ReqresUnknown().get_unknown_list()).raise_for_status()
        model.is_valid(model=ResourceListResponseDto, response=response.json())
