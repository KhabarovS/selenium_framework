from pathlib import Path

WEB_DRIVERS_DIR = Path('web') / 'drivers'
TIMEOUT = 15


class ChromeConfig:
    """Класс для хранения конфигурации Chrome драйвера."""
    exec_path_win32 = WEB_DRIVERS_DIR / 'chromedriver.exe'
    exec_path_win64 = WEB_DRIVERS_DIR / 'chromedriver.exe'
    default_options = [
        '--window-size=1920,1080',
        '--ignore-certificate-errors',
        '--disable-gpu',
        '--no-sandbox',
        'lang=ru',
    ]


class SelenoidConfig:
    """Класс для хранения конфигурации Selenoid."""
    HUB_URL = "http://localhost:4444/wd/hub"
    CLIPBOARD_URL = "http://localhost:8080/ws/clipboard/"
    DOWNLOAD_URL = "http://localhost:4444/download/"
    CAPABILITIES = {
        'chrome': {
            'browserName': 'chrome',
            'browserVersion': '119.0',

            'selenoid:options': {'enableVNC': True, 'enableVideo': False}
        },
    }
