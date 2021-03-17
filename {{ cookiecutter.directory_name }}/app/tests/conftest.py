"""Standard pytest fixtures used across all app tests"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

# `models` is necessary to ensure that AlchemyBase is properly populated
from app import models
from app.db import AlchemyBase
from app.environment import settings


@pytest.fixture(scope="session", autouse=True)
def session_local():
    """Override the default database with our testing database based off most recent models"""
    test_engine = create_engine(settings.postgres_url(), echo=False)
    # Drop database and recreate to ensure tests are always run against a clean slate
    if database_exists(test_engine.url):
        drop_database(test_engine.url)
    create_database(test_engine.url)
    # Create our local session handler
    TestSessionLocal = sessionmaker(bind=test_engine)
    # Create all tables
    AlchemyBase.metadata.create_all(bind=test_engine)
    try:
        yield TestSessionLocal
    finally:
        drop_database(test_engine.url)


@pytest.fixture(scope="function")
def session(session_local: Session, monkeypatch) -> Session:
    """Return an SQLAlchemy session for this test"""
    session = session_local()
    session.begin_nested()
    # Overwrite commits with flushes so that we can query stuff, but it's in the same transaction
    monkeypatch.setattr(session, "commit", session.flush)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
