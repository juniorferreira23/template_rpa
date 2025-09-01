#!/usr/bin/env python3

import argparse
import sqlite3
from time import sleep

from src.bots.bot_example import BotExample
from src.core.celery_app import celery_app
from src.core.settings import settings
from src.core.webdriver import get_webdriver


@celery_app.task
def hello(name: str) -> str:
    """Simples tarefa de saudação."""
    message = f'Olá, {name}'
    return message


@celery_app.task
def run_bot_example(headless_arg: bool) -> dict:
    driver = get_webdriver(headless=headless_arg)

    try:
        bot = BotExample(driver=driver)

        bot.navigate(url=settings.URL)

        bot.login(settings.LOGIN, settings.PASSWORD)

        diciplines = bot.get_disciplines()
        bot.navigate_to_payments()
        bot.navigate_to_attendance()
        sleep(3)
        windows = bot.get_windows()
        bot.change_window(windows[-1])
        bot.download_attendance_statement()

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS TASKS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                moment DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cursor.execute(
                """
            INSERT INTO TASKS (name)
            VALUES (?)
            """,
                ('teste',),
            )

            conn.commit()

        return {
            'message': 'Bot executed successfully',
            'disciplines': diciplines,
        }

    except Exception as err:
        raise err

    finally:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--headless', action='store_true', help='Executa o navegador oculto'
    )
    args = parser.parse_args()
    run_bot_example(headless_arg=args.headless)
