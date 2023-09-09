from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from allure import step, title

from other.config import Config
from other.logging import create_logger, logger
from web.driver_factory import Driver


def pytest_addoption(parser: pytest.Parser):
    """Парсер для аргументов командной строки и значений ini-файла.

    Args:
        parser: Инстанс Parser.
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер",
        choices=['chrome', 'yandex']
    )

    parser.addoption(
        "--headless",
        action="store_true",
        help="Укажите параметр, если хотите запустить браузер в headless режиме"
    )

    parser.addoption(
        "--selenoid",
        action="store_true",
        help="Укажите параметр, если хотите запустить браузер через Selenoid"
    )


def pytest_configure(config: pytest.Config):
    """Положить параметры запуска в окружение

    Args:        config: Config для доступа к значениям конфигурации, менеджеру плагинов и хукам плагинов
    """
    Config.log_level = config.getoption('--log_level')
    create_logger(log_level=Config.log_level)

    Config.web_url = config.getoption('--web_url')


@pytest.fixture(scope='session')
@title('Получить флаг запуска браузера в безоконном режиме')
def is_headless(request: SubRequest) -> bool:
    """Получить настройку "без окна" из параметров запуска, используется только для локального запуска!

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
    """
    return bool(request.config.getoption('--headless'))


@pytest.fixture(scope='session')
@title('Получить флаг запуска в SELENOID')
def is_selenoid(request: SubRequest) -> bool:
    """Получить настройку "Selenoid" из параметров запуска, используется для прогона с использованием SELENOID

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
    """
    return bool(request.config.getoption('--selenoid'))


@pytest.fixture(scope='session')
@title('Получить название браузера')
def browser_name(request: SubRequest) -> str:
    """Получить название браузера из параметров запуска

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
    """
    return request.config.getoption('--browser')


@pytest.fixture(scope='module', params=[()])
@title('Инициализировать драйвер с параметрами')
def driver(request: SubRequest, is_selenoid, browser_name):
    """Инициализировать экземпляр драйвера

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
        browser_name: Фикстура, имя браузера для прогона
        is_selenoid: Фикстура, Параметр запуска на удалённом сервере Selenoid
    """

    with step(f'Создать инстанс браузера {browser_name}, Selenoid={is_selenoid}'):
        Config.driver = Driver.get_driver(
            root=Path(request.config.rootpath),
            browser_name=browser_name,
            add_opts=[option for option in request.param],
            is_selenoid=is_selenoid
        )

    yield Config.driver

    try:
        Config.driver.quit()
        logger.info('Сессия драйвера закрыта!')

    except Exception:
        logger.warning('Сессия закрылась по таймауту!')
