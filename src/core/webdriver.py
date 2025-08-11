from pathlib import Path
from typing import List, Tuple, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

PATH_TEMP = Path(__file__).parent.parent.parent / 'tmp'
PATH_TEMP.parent.mkdir(parents=True, exist_ok=True)

TypeListOptions = Union[bool, List[str]]


list_options = [
    '--window-size=1366,768',
    '--enable_downloads=true',
    '--lang=pt-BR',
    '--no-sandbox',
    '--disable-extensions',
    '--disable-notifications',
    '--disable-dev-shm-usage',
    '--ignore-certificate-errors',
    '--disable-gpu',
    '--disable-blink-features=AutomationControlled',
    'user-agent=Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',  # noqa: E501
]

list_experimental_options: List = [
    ['excludeSwitches', ['enable-automation']],
    ['useAutomationExtension', False],
]

prefs = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False,
    'download.default_directory': str(PATH_TEMP),  # pasta de destino
    'download.prompt_for_download': False,  # não perguntar onde salvar
    'directory_upgrade': True,  # sobrescrever caso exista
    'safebrowsing.enabled': True,  # evita bloqueio de segurança
}


def inject_options(instance_options: Options, options_in: list[str]) -> None:
    for option in options_in:
        instance_options.add_argument(option)


def inject_experimental_options(
    instance_options: Options, options_in: List[Tuple[str, TypeListOptions]]
) -> None:
    for option in options_in:
        instance_options.add_experimental_option(option[0], option[1])


def inject_prefs(instance_options: Options, prefs_in: dict):
    instance_options.add_experimental_option('prefs', prefs_in)


def get_webdriver(
    default_options: bool = True,
    experimental_options: bool = True,
    default_prefs: bool = True,
    headless: bool = True,
    wait: int = 10,
) -> WebDriver:
    options = Options()

    if default_options:
        inject_options(options, list_options)

    if experimental_options:
        inject_experimental_options(options, list_experimental_options)

    if default_prefs:
        inject_prefs(options, prefs)

    if headless:
        options.add_argument('--headless=new')

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    )

    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {
            'source': """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            });
        """
        },
    )

    driver.implicitly_wait(wait)

    return driver
