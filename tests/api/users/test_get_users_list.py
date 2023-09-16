from allure import title, feature
from pytest import mark, param

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import UsersListResponseDto
from other import model
from tests.allure_constants import AllureApiUsers
from tests.constants import ERROR_STATUS_MSG


@feature('Проверить метод получения списка пользователей GET /api/users')
class TestGetUsersList(AllureApiUsers):

    @title('Получить список пользователей с валидными параметрами')
    @mark.parametrize('page', ['1', '2'])
    def test_get_users_list(self, page):
        (response := ReqresUsers().get_users(params={'page': page})).raise_for_status()
        model.is_valid(model=UsersListResponseDto, response=response.json())

    @title('[-] Получить список с невалидными параметрами')
    @mark.parametrize(
        'page', [
            param('один', marks=mark.bug),
            param(0, marks=mark.bug),
            param(-1, marks=mark.bug)
        ]
    )
    @mark.xfail(reason='Баг')
    def test_get_users_list_negative(self, page):
        response = ReqresUsers().get_users(params={'page': page})
        assert 400 == response.status_code, ERROR_STATUS_MSG.format(code=400, fact_code=response.status_code)
