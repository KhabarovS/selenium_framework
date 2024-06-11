import sys
from pathlib import Path

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
            is_remote: bool,
            is_headless: bool,
            add_opts: list[str] | None = None
    ) -> Remote | Chrome:
        """Создать экземпляр Chrome драйвера

        Args:
            root: корень проекта
            add_opts: дополнительные опции
            is_remote: запуск через удаленный браузер
        """
        options = ChromeOptions()

        for arg in ChromeConfig.default_options + add_opts:
            options.add_argument(arg)

        for name, opt in SelenoidConfig.CAPABILITIES['chrome'].items():
            options.set_capability(name, opt)

        if is_headless:
            options.add_argument("--headless")

        if is_remote:
            return Remote(
                command_executor=SelenoidConfig.HUB_URL,
                options=options,
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
            is_remote: bool,
            is_headless: bool,
            add_opts: list[str] | None = None,
    ) -> Remote | Chrome:
        """Получить экземпляр драйвера

        Args:
            root: путь до корня проекта
            is_remote: запуск через удаленный браузер
            is_headless: запуск в headless режиме
            browser_name: название браузера
            add_opts: дополнительные опции
        """
        logger.info(
            f'Переданы настройки браузера:\n'
            f'\tБраузер:       \t{browser_name}\n'
            f'\tДоп. настройки:\t{add_opts}\n'
            f'\tis_remote:      \t{is_remote}'
            f'\tis_headless:      \t{is_headless}'
        )
        return {
            'chrome': Driver.__create_chrome_driver
        }[browser_name](root=root, add_opts=add_opts, is_remote=is_remote, is_headless=is_headless)
