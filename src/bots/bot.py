from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from src.core.log import logger


class Bot:
    def __init__(self, driver: WebDriver, wait_explicit: int = 30):
        self.driver = driver
        self.wait = wait_explicit

    def _wait_for(self, condition):
        return WebDriverWait(self.driver, self.wait).until(condition)

    def _snapshot(self, step: str = 'error'):
        self.driver.save_screenshot(f'./tmp/snap_{step}.png')
        with open(f'./tmp/html_{step}.html', 'w', encoding='utf-8') as f:
            f.write(self.driver.page_source)

    def navigate(self, url: str):
        self.driver.get(url)
        logger.info(f'navigate to {url} successful')

    def get_windows(self) -> list[str]:
        windows = self.driver.window_handles
        logger.info(f'get windows {windows}')
        return windows

    def change_window(self, window: str):
        self.driver.switch_to.window(window)
        logger.info('change window successful')
