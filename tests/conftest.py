from _pytest.fixtures import SubRequest
from allure import step, title
from pytest import fixture
from selenium.webdriver.remote.webdriver import WebDriver

from other.logging import logger


@fixture(scope='session')
@title('Открыть страницу')
def open_page(request: SubRequest, driver: WebDriver) -> WebDriver:
    """Открыть вебдрайвер и страницу.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры;
        driver: экземпляр вебдрайвера.
    """
    if not (param := getattr(request, 'param', None)):
        logger.error(msg := f'В фикстуру не переданы обязательные параметры через indirect: page')
        raise RuntimeError(msg)

    with step(msg := f'Открыть страницу {param}'):
        logger.info(msg)
        page = param(driver=driver)
        page.get()

    yield page
