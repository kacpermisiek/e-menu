from enum import Enum


class LoggingLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    WARNING = "WARNING"


class UpdateMethod(str, Enum):
    PATCH = "PATCH"
    PUT = "PUT"
