import uuid

from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.main import app
from app.models.menu import MenuPosition
from app.settings import settings


@pytest.fixture(autouse=True)
def db_init(engine):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def test_client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def engine():
    engine = create_engine(settings.database.get_secret_value())
    assert engine is not None
    return engine


@pytest.fixture
def db_session(engine):
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        sess = local_session()
        try:
            yield sess
        finally:
            sess.close()

    return get_db


@pytest.fixture()
def db_api(db_session):
    s = db_session()
    yield next(s)
    s.close()


@pytest.fixture
def json_basic_menu_position() -> dict[str, Any]:
    return {
        "name": "test_menu",
        "price": 10.0,
        "description": "test_description",
        "preparation_time": 10,
        "is_vegan": False,
    }


@pytest.fixture
def json_basic_menu() -> dict[str, Any]:
    return {
        "name": "test_menu",
    }


@pytest.fixture
def with_menu_position(db_api, json_basic_menu_position):
    identifier = uuid.uuid4()
    db_api.add(MenuPosition(**json_basic_menu_position | {"id": identifier}))
    db_api.commit()
    return identifier
