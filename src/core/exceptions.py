from functools import wraps

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    ElementNotVisibleException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

from src.core.log import logger


def handle_exceptions_selenium(func):
    """Decorador para exceções do selenium

    Args:
        func (def): Função envelopada

    Raises:
        err (Exception): err

    Returns:
        _type_: wrapper
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except (NoSuchElementException, ElementNotVisibleException) as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'elemento não encontrado ou não visível - '
                f'{func.__name__} - {err}',
                exc_info=True,
            )
            raise err

        except (
            ElementClickInterceptedException,
            ElementNotInteractableException,
        ) as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                (
                    f'elemento não clicável ou não interativo - '
                    f'{func.__name__} - {err}'
                ),
                exc_info=True,
            )
            raise err

        except StaleElementReferenceException as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'referência de elemento obsoleto - {func.__name__} - {err}',
                exc_info=True,
            )
            raise err

        except TimeoutException as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'tempo de busca expirado - {func.__name__} - {err}',
                exc_info=True,
            )
            raise err

        except Exception as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'exceção não tratada - {func.__name__} - {err}', exc_info=True
            )
            raise err

    return wrapper
