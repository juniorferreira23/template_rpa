import os
import time
from functools import wraps

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.core.log import logger
from src.core.paths import PATH_TEMP


def wait_for_download(path_folder=None, timeout=60):
    """Espera a pasta receber o arquivo que está sendo baixado

    Args:
        path_folder (_type_, optional): caminho da pasta. Defaults to None.
        timeout (int, optional): tempo de espera. Defaults to 60.

    Raises:
        TimeoutError: tempo expirado

    Returns:
        _type_: _description_
    """
    if path_folder is None:
        path_folder = str(PATH_TEMP)

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            before_files = set(os.listdir(path_folder))
            result = func(self, *args, **kwargs)
            start_time = time.time()
            while time.time() - start_time < timeout:
                after_files = set(os.listdir(path_folder))
                new_files = after_files - before_files
                # Verifica se há algum novo arquivo que não seja .tmp
                # e .crdownload
                for f in new_files:
                    if not f.endswith('.tmp') and not f.endswith(
                        '.crdownload'
                    ):
                        return result
                time.sleep(1)
            raise TimeoutError('download not completed')

        return wrapper

    return decorator


class Bot:
    """Classe Pai dos bots, todos os bot herdam de Bot"""

    def __init__(self, driver: WebDriver, wait_explicit: int = 60):
        self.driver = driver
        self.wait = wait_explicit

    def _wait_for(self, condition):
        """busca por elementos com EC"""
        return WebDriverWait(self.driver, self.wait).until(condition)

    def _snapshot(self, step: str = 'error'):
        """printa a tela do navegador"""
        self.driver.save_screenshot(f'{PATH_TEMP}/snap_{step}.png')
        with open(f'{PATH_TEMP}/html_{step}.html', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

    def navigate(self, url: str):
        """navega para a url desejada

        Args:
            url (str): url de navegação
        """
        self.driver.get(url)
        logger.info(f'navigate to {url} successful')

    def get_windows(self) -> list[str]:
        """pega as abas abertas no navegador"""
        windows = self.driver.window_handles
        logger.info(f'get windows {windows}')
        return windows

    def change_window(self, window: str):
        """troca de aba

        Args:
            window (str): aba
        """
        self.driver.switch_to.window(window)
        logger.info('change window successful')

    def handle_alerts(self):
        """Lida com os alertas"""
        try:
            WebDriverWait(self.driver, self.wait).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            logger.info('Alerta aceito com sucesso.')
        except Exception as e:
            logger.error(f'Erro ao lidar com o alerta: {e}')
