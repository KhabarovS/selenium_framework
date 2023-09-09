import sys
from pathlib import Path
from typing import Optional, Union

from selenium.webdriver import Chrome, Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService

from other.logging import logger
from web.driver_config import ChromeConfig, SelenoidConfig


class Driver:
    """Класс для создания экземпляров различных браузеров"""

    @staticmethod
    def __create_chrome_driver(
            root: Path,
            add_opts: Optional[list] = None,
            is_selenoid: Optional[bool] = None
    ) -> Optional[Remote, Chrome]:
        """Создать экземпляр Chrome драйвера

        Args:
            root: корень проекта
            add_opts: дополнительные опции
            is_selenoid: запуск через Selenoid
        """
        options = ChromeOptions()

        for arg in ChromeConfig.default_options + add_opts:
            options.add_argument(arg)

        if is_selenoid:
            return Remote(
                command_executor=SelenoidConfig.HUB_URL,
                desired_capabilities=SelenoidConfig.CAPABILITIES['chrome'],
                options=options
            )

        else:
            return Chrome(
                service=ChromeService(executable_path=root / getattr(ChromeConfig, f'exec_path_{sys.platform}')),
                options=options
            )

    @staticmethod
    def get_driver(
            root: Path,
            browser_name: str,
            add_opts: Optional[list] = None,
            is_selenoid: Optional[bool] = None
    ) -> Union[Remote, Chrome]:
        """Получить экземпляр драйвера

        Args:
            root: путь до корня проекта
            is_selenoid: запуск через Selenoid
            browser_name: название браузера
            add_opts: дополнительные опции
        """
        logger.info(
            f'Переданы настройки браузера:\n'
            f'\tБраузер:       \t{browser_name}\n'
            f'\tДоп. настройки:\t{add_opts}\n'
            f'\tSelenoid:      \t{is_selenoid}'
        )
        return {
            'chrome': Driver.__create_chrome_driver
        }[browser_name](root=root, add_opts=add_opts, is_selenoid=is_selenoid)
