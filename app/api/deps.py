import base64
from typing import Iterator

from sqlalchemy.orm import Session

from app.db import get_session
from app.settings import settings


def get_db():
    def inner() -> Iterator[Session]:
        db = get_session(settings.database)
        try:
            yield db
        finally:
            db.close()

    return inner


def get_encryption_key():
    return base64.urlsafe_b64encode(
        bytes.fromhex(settings.encryption_key.get_secret_value())
    )
