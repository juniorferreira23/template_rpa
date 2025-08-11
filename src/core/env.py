import os

from dotenv import load_dotenv

load_dotenv()


class Env:
    URL = os.getenv('URL')
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    LOGIN_EMAIL = os.getenv('LOGIN_EMAIL')
    PASSWORD_EMAIL = os.getenv('PASSWORD_EMAIL')
    RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS')
    RECIPIENT_EMAILS = (
        RECIPIENT_EMAILS.split(',') if RECIPIENT_EMAILS else []
    )


env = Env()
