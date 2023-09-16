from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import UserResponseDto
from other import model
from tests.allure_constants import AllureApiUsers
from tests.constants import ERROR_STATUS_MSG


@feature('Проверить метод получения пользователей GET /api/users/{user_id}')
class TestGetSingleUser(AllureApiUsers):

    @title('Получить  пользователя с валидными параметрами')
    @mark.parametrize('user_id', [1, 2])
    def test_get_single_user(self, user_id):
        (response := ReqresUsers().get_single_user(user_id=user_id)).raise_for_status()
        model.is_valid(model=UserResponseDto, response=response.json())

    @title('Получить  пользователя с валидными параметрами NOT FOUND')
    @mark.parametrize('user_id', [23, 55])
    def test_get__user_not_found(self, user_id):
        response = ReqresUsers().get_single_user(user_id=user_id)
        assert 404 == response.status_code, ERROR_STATUS_MSG.format(code=404, fact_code=response.status_code)
        assert '{}' == response.text, f'Тело ответа "{response.text}" не соответствует ожидаемому {{}}'

    @title('[-] Получить пользователя невалидным идентификатором')
    @mark.parametrize(
        'user_id', [
            param('один', marks=mark.bug),
            param(0, marks=mark.bug),
            param(-1, marks=mark.bug)
        ]
    )
    @mark.xfail(reason='Баг')
    def test_get_users_list_negative(self, user_id):
        response = ReqresUsers().get_single_user(user_id=user_id)
        assert 400 == response.status_code, ERROR_STATUS_MSG.format(code=400, fact_code=response.status_code)
