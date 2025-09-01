from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='ignore'
    )

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_URL: str

    URL: str
    LOGIN: str
    PASSWORD: str

    LOGIN_EMAIL: str
    PASSWORD_EMAIL: str
    RECIPIENT_EMAILS: str


settings = Settings()  # type: ignore
