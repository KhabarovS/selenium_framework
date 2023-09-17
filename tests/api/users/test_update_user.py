from allure import feature, title
from pytest import mark

from api.frame_request import MethodEnum
from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto, UpdateUserDto
from other import model
from other.random_values import get_random_job, get_random_name
from tests.allure_constants import AllureApiUsers
from tests.constants import ERROR_STATUS_MSG


@feature('Обновить пользователя PATCH/PUT /api/users')
class TestUpdateUser(AllureApiUsers):

    @title('Частично обновить пользователя')
    @mark.bug
    @mark.xfail
    def test_patch_user(self, fixture_create_user: CreateUserDto):
        response = ReqresUsers().update_user(
            method=MethodEnum.PATCH,
            user_id=fixture_create_user.id_,
            json={'name': get_random_name()}
        )

        assert 200 == response.status_code, ERROR_STATUS_MSG.format(code=200, fact_code=response.status_code)
        model.is_valid(model=UpdateUserDto, response=response.json())

    @title('Обновить пользователя')
    def test_put_user(self, fixture_create_user: CreateUserDto):
        response = ReqresUsers().update_user(
            method=MethodEnum.PATCH,
            user_id=fixture_create_user.id_,
            json={'name': get_random_name(), 'job': get_random_job()}
        )
        assert 200 == response.status_code, ERROR_STATUS_MSG.format(code=200, fact_code=response.status_code)
        model.is_valid(model=UpdateUserDto, response=response.json())