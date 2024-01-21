from allure import feature, title
from pytest import mark

from api.services.reqres_in.login import ReqresLogin
from dto.register_dto import RegisterResponse
from other import model
from other.random_values import get_random_email, get_random_string
from tests.allure_constants import AllureApiLogin
from tests.constants import ERROR_STATUS_MSG


@feature('Проверить метод логина пользователя')
class TestLoginUser(AllureApiLogin):

    @title('Логин пользователя с валидными данными')
    def test_login_user(self):
        response_obj = ReqresLogin().post_login(json={'email': 'eve.holt@reqres.in', 'password': 'cityslicka'})

        response_obj.raise_for_status()
        response_obj.check_is_valid()

    @title('[-] Логин пользователя с невалидными данными')
    @mark.parametrize(
        'json, msg', [
            ({'email': get_random_email()}, 'Missing password'),
            ({'password': get_random_string()}, 'Missing email or username'),
            ({}, 'Missing email or username')
        ]
    )
    def test_login_user_unsuccessful(self, json: dict, msg: str):
        response = ReqresLogin().post_login(json=json)

        assert 400 == response.status_code, ERROR_STATUS_MSG.format(code=400, fact_code=response.status_code)
        model.is_valid(model=RegisterResponse, response=(content := response.json()))
        assert msg == content['error']
