import os

from dotenv import load_dotenv

load_dotenv()


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Variável de ambiente '{name}' não definida.")
    return value


class Env:
    USER_RABBITMQ = get_env_var('RABBITMQ_DEFAULT_USER')
    PASSWORD_RABBITMQ = get_env_var('RABBITMQ_DEFAULT_PASS')

    URL = get_env_var('URL')
    LOGIN = get_env_var('LOGIN')
    PASSWORD = get_env_var('PASSWORD')

    LOGIN_EMAIL = get_env_var('LOGIN_EMAIL')
    PASSWORD_EMAIL = get_env_var('PASSWORD_EMAIL')
    RECIPIENT_EMAILS = get_env_var('RECIPIENT_EMAILS')
    RECIPIENT_EMAILS = RECIPIENT_EMAILS.split(',') if RECIPIENT_EMAILS else []


env = Env()
