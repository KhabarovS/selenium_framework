from typing import Iterable

from _pytest.fixtures import SubRequest
from allure import step, title
from pytest import fixture
from selenium.webdriver.remote.webdriver import WebDriver

from other.logging import logger


@fixture
@title('Открыть страницу')
def open_page(request: SubRequest, driver: WebDriver):
    """Открыть вебдрайвер и страницу.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры;
        driver: экземпляр вебдрайвера.
    """
    if not (param := getattr(request, 'param', None)):
        logger.error(msg := f'В фикстуру не переданы обязательные параметры через indirect: user, page')
        raise RuntimeError(msg)

    if len(param) != 2 or not isinstance(param, Iterable):
        logger.error(msg := 'В фикстуру передано неверное количество параметров через indirect: user, page')
        raise RuntimeError(msg)

    user, page = param

    with step(msg := f'Открыть страницу {page}'):
        logger.info(msg)
        page = page(driver=driver)
        page.get()

    yield page
