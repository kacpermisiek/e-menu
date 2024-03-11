from pydantic import SecretStr
from pydantic_settings import BaseSettings

from app.utils.enums import LoggingLevel


class Settings(BaseSettings):
    log_level: LoggingLevel = LoggingLevel.DEBUG
    version: str = "dev"

    encryption_key: SecretStr = SecretStr(
        "7fc1ec811e9b0271f7d2e9a848a39afb6110a88aa14e8b017d39349e32922901"
    )  # This should be changed in production

    database: SecretStr = SecretStr("postgresql://alice:xyz@localhost:5432/menu")

    currency: str = "PLN"

    email_sender_name: str = "eMenu"

    smtp_enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465
    smtp_user: str = "smtp_user"
    smtp_password: SecretStr = SecretStr("smtp_password")


settings = Settings()
