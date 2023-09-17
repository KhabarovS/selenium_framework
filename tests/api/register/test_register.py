from allure import feature, title
from pytest import mark, param

from api.services.reqres_in.register import ReqresRegister
from dto.register_dto import RegisterResponse
from other import model
from other.random_values import get_random_email, get_random_string
from tests.allure_constants import AllureApiRegister
from tests.constants import ERROR_STATUS_MSG


@feature('Проверить метод регистрации пользователя')
class TestRegister(AllureApiRegister):

    @title('Регистрация пользователя')
    @mark.parametrize(
        'email, password', [
            param(get_random_email(), get_random_string(), marks=(mark.bug, mark.xfail)),
            param('eve.holt@reqres.in', 'pistol')
        ]
    )
    def test_register_user(self, email: str, password: str):
        (
            response := ReqresRegister().post_register(json={'email': email, 'password': password})
        ).raise_for_status()

        model.is_valid(model=RegisterResponse, response=response.json())

    @title('[-] Регистрация пользователя с невалидными данными')
    @mark.parametrize(
        'json, msg', [
            ({'email': get_random_email()}, 'Missing password'),
            ({'password': get_random_string()}, 'Missing email or username'),
            ({}, 'Missing email or username')
        ]
    )
    def test_register_unsuccessful_user(self, json: dict, msg: str):
        response = ReqresRegister().post_register(json=json)

        assert 400 == response.status_code, ERROR_STATUS_MSG.format(code=400, fact_code=response.status_code)
        model.is_valid(model=RegisterResponse, response=(content := response.json()))
        assert msg == content['error']
