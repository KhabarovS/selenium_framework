from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from allure import attach, attachment_type, step, title

from other.config import Config
from other.logging import create_logger, logger
from web.driver_factory import Driver


def pytest_addoption(parser: pytest.Parser):
    """Парсер для аргументов командной строки.

    Args:
        parser: Инстанс Parser.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер",
        choices=['chrome']
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Укажите параметр, если хотите запустить браузер в headless режиме"
    )

    parser.addoption(
        "--remote",
        action="store_true",
        help="Укажите параметр, если хотите запустить удаленный браузер"
    )

    parser.addoption(
        "--log_level",
        action='store',
        default='INFO',
        help='Уровень логгирования',
        choices=['DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    )

    parser.addoption(
        "--web_url",
        action='store',
        help='Базовый URL WEB-страниц'
    )


def pytest_configure(config: pytest.Config):
    """Положить параметры запуска в окружение

    Args: config: Config для доступа к значениям конфигурации, менеджеру плагинов и хукам плагинов
    """
    Config.log_level = config.getoption('--log_level')
    create_logger(log_level=Config.log_level)

    Config.is_remote = config.getoption('--remote')
    Config.is_headless = config.getoption('--headless')
    Config.browser = config.getoption('--browser')
    Config.web_url = config.getoption('--web_url')


@pytest.fixture(scope='session', params=[()])
@title('Инициализировать драйвер с параметрами')
def driver(request: SubRequest):
    """Инициализировать экземпляр драйвера

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
    """

    with step(f'Создать экземпляр браузера {Config.browser}, Remote={Config.is_remote}'):
        Config.driver = Driver.get_driver(
            root=Path(request.config.rootpath),
            browser_name=Config.browser,
            add_opts=[option for option in request.param],
            is_remote=Config.is_remote,
            is_headless=Config.is_headless,
        )

    yield Config.driver

    try:
        Config.driver.quit()
        logger.info('Сессия драйвера закрыта!')

    except TimeoutError:
        logger.warning('Сессия закрылась по таймауту!')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: Function, call: CallInfo): # noqa
    """Хук для сохранения скриншота при падении

    Args:
        item: выполненный тест
        call: объект с информацией о вызове функции

    Returns:

    """
    outcome = yield
    rep: TestReport = outcome.get_result()

    if (
            rep.when == 'call'
            and any(map(lambda x: x in item.fixturenames, ['driver', 'open_page']))
            and rep.failed
    ):

        try:
            logger.info(f'Сохранить скриншот при падении теста: {rep.nodeid}')
            attach(
                name=f'screenshot_{rep.nodeid}',
                body=Config.driver.get_screenshot_as_png(),
                attachment_type=attachment_type.PNG
            )
            logger.info(f'Скриншот успешно сохранен')

        except Exception:
            logger.warning('Не удалось сохранить скриншот')
