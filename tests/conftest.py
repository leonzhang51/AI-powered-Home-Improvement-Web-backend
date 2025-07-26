"""
Test configuration and fixtures.
"""
import pytest
import asyncio
import os
import tempfile
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment before any app imports
os.environ["DATABASE_URL"] = "sqlite:///./test_temp.db"

# Import models so they're registered with Base.metadata
from app.models.models import User, Project, Rendering, ProjectPlan, ShoppingList, AgentSession
from app.db.database import Base, get_db
from app.core.config import Settings
from main import app

# Create test database engine
test_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
test_db_file.close()
SQLALCHEMY_DATABASE_URL = f"sqlite:///{test_db_file.name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db():
    """Create a database session for testing."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db) -> Generator:
    """Create a test client."""
    with TestClient(app) as c:
        yield c
