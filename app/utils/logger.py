import logging
import sys
from typing import Any

import structlog

from .enums import LoggingLevel


def setup_logger(log_level: LoggingLevel) -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=log_level.value)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,  # this has to be 'firster'!
            structlog.processors.TimeStamper(utc=True),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.StackInfoRenderer(),
            structlog.stdlib.ExtraAdder(),
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    root_logger = structlog.get_logger("root")

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        root_logger.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


def get_logger(name: str) -> Any:
    return structlog.stdlib.get_logger(name)
