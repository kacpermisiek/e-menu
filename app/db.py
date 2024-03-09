from typing import Any

from pydantic import SecretStr
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
Meta = MetaData()


def get_session(database_dsn: SecretStr) -> Any:
    session_constructor = get_session_constructor(database_dsn)
    session = session_constructor()
    return session


def get_session_constructor(database_dsn: SecretStr) -> Any:
    engine = prepare_database(database_dsn)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def prepare_database(database_dsn: SecretStr) -> Any:
    return create_engine(
        database_dsn.get_secret_value(),
    )
