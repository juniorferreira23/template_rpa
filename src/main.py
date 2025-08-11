#!/usr/bin/env python3

import argparse
from time import sleep

from src.bots.bot_example import BotExample
from src.core.env import env
from src.core.webdriver import get_webdriver


def main(headless_arg: bool):
    driver = get_webdriver(headless=headless_arg)

    try:
        bot = BotExample(driver=driver)

        if env.URL is None:
            raise ValueError('env.URL is not set')
        bot.navigate(url=env.URL)

        if env.LOGIN is None or env.PASSWORD is None:
            raise ValueError('env.LOGIN and env.PASSWORD must be set')
        bot.login(env.LOGIN, env.PASSWORD)

        bot.get_disciplines()
        bot.navigate_to_payments()
        bot.navigate_to_attendance()
        sleep(3)
        windows = bot.get_windows()
        bot.change_window(windows[-1])
        bot.download_attendance_statement()

        sleep(30)

    except Exception as err:
        print(err)

    finally:
        driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Executa o navegador oculto'
    )
    args = parser.parse_args()
    main(headless_arg=args.headless)
