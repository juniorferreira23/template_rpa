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


def handle_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)

        except (NoSuchElementException, ElementNotVisibleException) as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'Element not found or not visible - {func.__name__} - {err}',
                exc_info=True,
            )
            raise

        except (
            ElementClickInterceptedException,
            ElementNotInteractableException,
        ) as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                (
                    f'Element not clickable or not interactable - '
                    f'{func.__name__} - {err}'
                ),
                exc_info=True,
            )
            raise

        except StaleElementReferenceException as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'Stale element reference - {func.__name__} - {err}',
                exc_info=True,
            )
            raise

        except TimeoutException as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'Time out - {func.__name__} - {err}',
                exc_info=True,
            )
            raise

        except Exception as err:
            if hasattr(self, '_snapshot'):
                self._snapshot(func.__name__)
            logger.error(
                f'Unhandled exception - {func.__name__} - {err}', exc_info=True
            )
            raise

    return wrapper
