from _pytest.fixtures import SubRequest
from pytest import fixture

from api.services.reqres_in.users import ReqresUsers
from dto.users_dto import CreateUserDto
from other.random_values import get_random_name, get_random_job


@fixture(params=[{'delete_after': True}])
def fixture_create_user(request: SubRequest) -> CreateUserDto:
    """ Фикстура для создания пользователя и удаления"""

    delete_after = request.param['delete_after']
    (
        response := ReqresUsers().create_user(json={'name': get_random_name(), 'job': get_random_job()})
    ).raise_for_status()

    yield (user := CreateUserDto(**response.json()))

    if delete_after:
        ReqresUsers().delete_user(user_id=user.id_).raise_for_status()


@fixture
def fixture_delete_user() -> list:
    user_ids: list[int] = []

    yield user_ids

    [ReqresUsers().delete_user(user_id=id_).raise_for_status() for id_ in user_ids]
