from typing import List, Union

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from src.core.paths import PATH_TEMP

PATH_TEMP.parent.mkdir(parents=True, exist_ok=True)

TypeListOptions = Union[bool, List[str]]


list_options = [
    '--enable_downloads=true',
    '--lang=pt-BR',
    '--no-sandbox',
    '--disable-extensions',
    '--disable-notifications',
    '--disable-dev-shm-usage',
    '--ignore-certificate-errors',
    '--disable-gpu',
    '--disable-blink-features=AutomationControlled',
    (
        'user-agent=Mozilla/5.0 (Windows NT 11.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/138.0.0.0 Safari/537.36'
    ),
]

prefs = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
    'download.default_directory': str(PATH_TEMP),  # pasta de destino
    'download.prompt_for_download': False,  # não perguntar onde salvar
    'directory_upgrade': True,  # sobrescrever caso exista
    'safebrowsing.enabled': True,  # evita bloqueio de segurança
    'profile.default_content_setting_values.geolocation': 2,  # block geo
}


def inject_options(
    instance_options: Union[Options, uc.ChromeOptions], options_in: list[str]
) -> None:
    for option in options_in:
        instance_options.add_argument(option)


def inject_prefs(
    instance_options: Union[Options, uc.ChromeOptions], prefs_in: dict
):
    instance_options.add_experimental_option('prefs', prefs_in)


def get_webdriver(
    default_options: bool = True,
    default_prefs: bool = True,
    headless: bool = True,
    wait: int = 10,
) -> WebDriver:
    options = uc.ChromeOptions()

    if default_options:
        inject_options(options, list_options)

    if default_prefs:
        inject_prefs(options, prefs)

    if headless:
        options.add_argument('--headless=new')

    driver = uc.Chrome(options=options, headless=headless, use_subprocess=True)
    driver.set_window_size(1366, 768)

    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            'source': """
            Object.defineProperty(
                navigator,
                'webdriver',
                { get: () => undefined }
            );
            Object.defineProperty(
                navigator,
                'plugins',
                { get: () => [1, 2, 3, 4, 5] }
            );
            Object.defineProperty(
                navigator,
                'languages',
                { get: () => ['pt-BR', 'pt'] }
            );
            """
        },
    )

    driver.implicitly_wait(wait)

    return driver
