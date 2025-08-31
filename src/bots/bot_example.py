from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from src.bots.bot import Bot
from src.core.exceptions import handle_exceptions_selenium
from src.core.log import logger


class BotExample(Bot):
    def __init__(self, driver: WebDriver, wait_explicit: int = 30):
        super().__init__(driver, wait_explicit)

    @handle_exceptions_selenium
    def login(self, username: str, password: str):
        login_field = self.driver.find_element(By.ID, 'userNameInput')
        login_field.send_keys(username)
        password_field = self.driver.find_element(By.ID, 'passwordInput')
        password_field.send_keys(password, Keys.ENTER)

        logger.info('login successful')

    @handle_exceptions_selenium
    def get_disciplines(self):
        container_span = self.driver.find_element(
            By.ID,
            (
                'wt100_wt21_wtMainContent_wtMainContent_wt268_SatinUIFr'
                'amework_wtwbDisciplinas_block_wtList_disciplinasAtual'
            ),
        )

        diciplines = container_span.find_elements(
            By.XPATH,
            './/span//div[@class="containerDisciplinasNotas"]//a//span',
        )

        for i in diciplines:
            print(i.text)

        logger.info('get disciplines successful')
        return [d.text for d in diciplines]

    @handle_exceptions_selenium
    def navigate_to_payments(self):
        button_digital_wallet = self._wait_for(
            EC.element_to_be_clickable((
                By.ID,
                'wt100_wt21_wtMenu_wt9_wtFINANCEIRO2_wtPlaceholder1',
            ))
        )
        button_digital_wallet.click()

        button_payments = self._wait_for(
            EC.element_to_be_clickable((
                By.ID,
                'wt100_wt21_wtMenu_wt9_wt18_wtPagamentos_wtPlaceholder1',
            ))
        )
        button_payments.click()

        logger.info('navigate to payments successful')

    @handle_exceptions_selenium
    def navigate_to_attendance(self):
        button_request = self.driver.find_element(
            By.ID, 'wt15_wt21_wtMenu_wt9_wtSolicitacoesMenu'
        )
        button_request.click()
        button_declaration = self.driver.find_element(
            By.ID, 'wt15_wt21_wtMenu_wt9_wt92_wt342_wtPlaceholder1'
        )
        button_declaration.click()

        logger.info('navigate to declaration successful')

    @handle_exceptions_selenium
    def download_attendance_statement(self):
        element = self._wait_for(
            EC.element_to_be_clickable((
                By.ID,
                (
                    'Aluno_wt2_block_wt21_wtMainContent_wtMa'
                    'inContent_wtDeclaracoesEHistoricos_OutSy'
                    'stemsUIWeb_wtTabs_block_wtTabs_Content_Ou'
                    'tSystemsUIWeb_wtContentOne_block_wtContent_wt96'
                ),
            ))
        )
        element.click()

        logger.info('download attendance statement successful')
