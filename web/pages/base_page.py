from allure import step
from selenium.common import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from other.config import Config
from other.logging import logger
from web import driver_config
from web.locator import Locator, format_locator


class BasePage:
    """ Базовый класс страницы для работы с элементами """

    def __init__(self, driver: WebDriver):
        """

        Args:
            driver: экземпляр драйвера
        """
        self._driver = driver
        self.url = Config.web_url

    @property
    def current_url(self) -> str:
        """ Получить текущий url """
        return self._driver.current_url

    @property
    def driver(self) -> WebDriver:
        """ Получить экземпляр драйвера """
        return self._driver

    @step('Открыть url класса')
    def get(self):
        """ Перейти по ссылке класса """
        logger.info(f'Открываем страницу {self.url}')
        self._driver.get(self.url)
        logger.success(f'Страница {self.url} открыта')

    @step('Открыть страницу по url')
    def open_page(self, url: str):
        """ Перейти по ссылке

        Args:
            url: ссылка
        """
        logger.info(f'Открываем страницу {url}')
        self._driver.get(url)
        logger.success(f'Страница {url} url')

    @format_locator
    @step('Найти элемент по локатору')
    def find_element_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Ожидать присутствие элемента на странице

        Args:
            locator: локатор
            timeout: таймаут ожидания
        """
        try:
            logger.info(f'Ожидаем присутствия  элемента с локатором {locator} в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.presence_of_element_located(locator=locator.locator)
            )

            logger.success(f'Элемент {locator} найден')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Элемент {locator} не найден в течение {timeout}')
            e.args = msg,

            raise e

    @format_locator
    @step('Найти элементы на странице по локатору')
    def find_elements_by_locator(self, locator: Locator, **kwargs) -> list[WebElement]:
        """Найти список элементов на странице

        Args:
            locator: локатор
        """
        logger.info(f'Поиск локаторов {locator}')
        elements = self._driver.find_elements(*locator.locator)
        logger.success(f'Найдено {len(elements)} элементов по локатору {locator}')

        return elements

    @format_locator
    @step('Найти кликабельный элемент на странице')
    def find_clickable_element_by_locator(
            self,
            locator: Locator,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Ожидание кликабельности элемента

        Args:
            locator: локатор
            timeout: таймаут
        """
        try:
            logger.info(f'Ожидаем кликабельности элемента {locator} в течение {timeout}')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.element_to_be_clickable(mark=locator.locator)
            )

            logger.success('Локатор доступен для клика')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Локатор {locator} не стал кликабельным в течение {timeout}')
            e.args = msg,

            raise e

    @format_locator
    @step('Ожидать видимость элемента')
    def find_visible_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Ожидать присутствия элемента в DOM страницы и его видимости.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем видимый {locator} в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.visibility_of_element_located(locator=locator.locator)
            )
            logger.success('Элемент найден и виден!')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Не удалось найти видимый {locator} в течение {timeout} секунд')
            e.msg += f'\n{msg}'

            raise e

    @format_locator
    @step('Скролл страницы до элемента')
    def scroll_into_view_by_locator(
            self,
            locator: Locator,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Проскролить страницу до элемента

        Args:
            locator: локатор
            timeout: таймаут
        """
        logger.info('Скролить страницу до элемента')
        element = self.find_element_by_locator(locator=locator, timeout=timeout)
        self._driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.success('Страница прокручена до элемента')

        return element

    @format_locator
    @step('Кликнуть по элементу')
    def click_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Найти элемент и кликнуть по нему

        Args:
            locator: локатор
            timeout: таймаут
        """
        try:
            logger.info(f'Клик по элементу {locator}')
            element = self.find_clickable_element_by_locator(locator=locator, timeout=timeout)

            element.click()

            logger.success('Клик успешно выполнен')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось кликнуть по элементу {locator}')
            e.args = msg,

            raise e

    @format_locator
    @step('Ввести значение в элемент по локатору')
    def send_keys_by_locator(
            self,
            locator: Locator,
            keys: str,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Найти элемент по локатору и ввести в него значение

        Args:
            locator: локатор
            keys: текст для ввода
            timeout: таймаут
        """
        try:
            logger.info(f'Ввод значения в элемент {locator}')
            element = self.find_element_by_locator(locator=locator, timeout=timeout)
            element.send_keys(keys)
            logger.success('Значение успешно введено')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось ввести значение  {keys} в элемент {locator}')
            e.args = msg,

            raise e

    @format_locator
    @step('Очистить поле по локатору')
    def clear_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Очистить поле для ввода

        Args:
            locator: локатор
            timeout: таймаут
        """
        try:
            logger.info(f'Очистка элемента {locator}')
            (element := self.find_element_by_locator(locator=locator, timeout=timeout)).clear()
            logger.success(f'Элемент {locator} успешно очищен')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось очистить элемент {locator}')
            e.args = msg,

            raise e
