import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.settings import settings


@pytest.fixture(scope="module")
def engine():
    engine = None
    create_engine(settings.test_database.get_secret_value())
    assert engine is not None
    return engine


@pytest.fixture
def db_session(engine):
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    return get_db


@pytest.fixture()
def db_api(db_session):
    s = db_session()
    yield next(s)
    s.close()
