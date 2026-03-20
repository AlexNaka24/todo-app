import pytest

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from fastapi import status

from database import Base

from routers.auth import get_current_user
from routers.auth import get_current_user
from routers.todos import get_db

from main import app

import models

# Use a separate database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new engine for the test database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

# Create a new session for testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables for testing
Base.metadata.create_all(bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the get_current_user dependency to return a test user
def override_get_current_user():
    return {"id": 1, "username": "testuser", "user_role": "admin"}

# Override the get_db dependency in the main application with the testing version
app.dependency_overrides[get_db] = override_get_db

# Override the get_current_user dependency in the main application with the testing version
app.dependency_overrides[get_current_user] = override_get_current_user

# Create a TestClient for testing the FastAPI application
client = TestClient(app)

# Fixture to set up a test todo item in the database before each test and clean up after the test
@pytest.fixture()
def test_todos():
    todo = models.todos(
        id=1,
        title="Test Todo",
        description="This is a test todo",
        completed=False,
        owner_id=1
    )

    # Add the test todo to the database
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    # Clean up the database after the test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

# Test case for getting all todos when authenticated
def test_all_authenticated(test_todos):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False,
        "owner_id": 1
    }]