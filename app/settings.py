from pydantic import SecretStr
from pydantic_settings import BaseSettings

from app.utils.enums import LoggingLevel


class Settings(BaseSettings):
    log_level: LoggingLevel = LoggingLevel.DEBUG
    version: str = "dev"

    encryption_key: SecretStr = SecretStr(
        "ad3be4c4c77d8a68624e9014e7df93c9d9c3b6dd401889a9fffe0e7f62e91189"
    )  # This should be changed in production
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    database: SecretStr = SecretStr("postgresql://alice:xyz@localhost:5432/menu")

    currency: str = "PLN"

    email_sender_name: str = "eMenu"

    smtp_enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str = "smtp_user"
    smtp_password: SecretStr = SecretStr("smtp_password")

    scheduler_timezone: str = "Europe/Warsaw"


settings = Settings()
