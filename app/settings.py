from pydantic import SecretStr
from pydantic_settings import BaseSettings

from app.utils.enums import LoggingLevel


class Settings(BaseSettings):
    log_level: LoggingLevel = LoggingLevel.DEBUG
    version: str = "dev"

    database: SecretStr = SecretStr("postgresql://alice:xyz@localhost:5432/menu")

    currency: str = "PLN"

    smtp_enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_user: str = "user"
    smtp_password: SecretStr = SecretStr("password")


settings = Settings()
