from pydantic import BaseSettings, SecretStr

from app.utils.enums import LoggingLevel


class Settings(BaseSettings):
    log_level: LoggingLevel = LoggingLevel.DEBUG
    version: str = "dev"

    database: SecretStr = SecretStr("postgresql://alice:xyz@localhost:5432/menu")


settings = Settings()
