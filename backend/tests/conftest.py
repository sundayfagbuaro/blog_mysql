from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# This is to include backend dir in sys.path so that we can import from db,main.py

from db.base import Base
from db.session import get_db
from apis.base import api_router


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app

SQLALCHEMY_DATABASE_URL =  "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Use connect_args parameters only with sqlite

SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)

@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """""
    create a fresh database on each test case
    """""
    Base.metadata.create_all(engine)      # Create the tables
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session    # Use the session in test
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """""
    create a new FastAPI TestClient that uses the db_session fixture to override the get_db
    dependency that is injected into route
    """""
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client





