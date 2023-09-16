from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto
from other import model
from other.random_values import get_random_name, get_random_job
from tests.allure_constants import AllureApiUsers
from tests.constants import ERROR_STATUS_MSG


@feature('Проверить метод создания пользователя POST /api/users')
class TestCreateUser(AllureApiUsers):

    @title('Создать пользователя с валидными параметрами')
    def test_create_user(self):
        response = ReqresUsers().create_user(json={'name': get_random_name(), 'job': get_random_job()})

        assert 201 == response.status_code, ERROR_STATUS_MSG.format(code=201, fact_code=response.status_code)
        model.is_valid(model=CreateUserDto, response=response.json())

    @title('[-] Создать пользователя с не валидными параметрами')
    @mark.parametrize(
        'json', [
            param({'name': '', 'job': get_random_job()}, marks=mark.bug),
            param({'name': get_random_name(), 'job': ''}, marks=mark.bug),
            param({'name': get_random_name()}, marks=mark.bug),
            param({'job': get_random_job()}, marks=mark.bug),
        ]
    )
    @mark.xfail
    def test_create_user_negative(self, json):
        response = ReqresUsers().create_user(json=json)
        assert 400 == response.status_code, ERROR_STATUS_MSG.format(code=400, fact_code=response.status_code)
