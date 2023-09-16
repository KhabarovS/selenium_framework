from allure import feature, title

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto
from tests.allure_constants import AllureApiUsers
from tests.constants import ERROR_STATUS_MSG


@feature('Удалить пользователя DELETE /api/users')
class TestDeleteUser(AllureApiUsers):

    @title('Удалить пользователя')
    def test_delete_user(self, fixture_create_user: CreateUserDto):
        response = ReqresUsers().delete_user(user_id=fixture_create_user.id_)

        assert 204 == response.status_code, ERROR_STATUS_MSG.format(code=204, fact_code=response.status_code)
