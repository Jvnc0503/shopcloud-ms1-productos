from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DEBUG", "False")
os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{Path(__file__).resolve().parent / 'ms1_test.db'}"

import pytest
from fastapi.testclient import TestClient

from src.database import Base, SessionLocal, engine
from src.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()