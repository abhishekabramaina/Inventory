import os
import pytest
from typing import Generator, Dict, Any

# Ensure test DB is used
os.environ["DATABASE_PATH"] = "test.db"

from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db_connection, initialize_db

@pytest.fixture(autouse=True)
def setup_test_db() -> Generator[None, None, None]:
    """Fixture to initialize a fresh database schema and clean it up after each test."""
    initialize_db()
    yield
    # Clean up table to prevent state leakage
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS items")
        conn.commit()
    finally:
        conn.close()
    
    # Remove test DB file
    if os.path.exists("test.db"):
        try:
            os.remove("test.db")
        except OSError:
            pass

@pytest.fixture
def item_factory() -> Any:
    """A data factory fixture to generate test item payloads with overrides."""
    def _create_item_payload(name: str = "Test Item", description: str | None = "Test Description") -> Dict[str, Any]:
        return {"name": name, "description": description}
    return _create_item_payload

class TestFastAPIApp:
    """Test suite for FastAPI endpoints and health status."""

    def test_health_check_returns_success(self) -> None:
        """Verifies that the root health check endpoint returns 200 and a success message."""
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok", "message": "Welcome to the FastAPI Practice App!"}

    def test_creates_item_when_valid_payload_provided(self, item_factory: Any) -> None:
        """Verifies that items can be created with valid name and description."""
        client = TestClient(app)
        payload = item_factory(name="A Valid Item", description="A valid description")
        
        response = client.post("/items/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == "A Valid Item"
        assert data["data"]["description"] == "A valid description"
        assert "id" in data["data"]

    def test_creates_item_with_only_name(self, item_factory: Any) -> None:
        """Verifies that description is optional when creating an item."""
        client = TestClient(app)
        payload = item_factory(name="Only Name Item", description=None)
        
        response = client.post("/items/", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == "Only Name Item"
        assert data["data"]["description"] is None

    def test_fails_creation_when_name_is_empty_or_whitespace(self, item_factory: Any) -> None:
        """Verifies that name is validated and cannot be whitespace-only."""
        client = TestClient(app)
        payload = item_factory(name="    ", description="some description")
        
        response = client.post("/items/", json=payload)
        assert response.status_code == 400
        assert response.json()["detail"] == "Item name cannot be empty or only whitespace."

    def test_retrieves_all_items_when_database_has_records(self, item_factory: Any) -> None:
        """Verifies that multiple created items are successfully listed by GET /items/."""
        client = TestClient(app)
        
        # Add a couple of items
        client.post("/items/", json=item_factory(name="First Item", description="First"))
        client.post("/items/", json=item_factory(name="Second Item", description="Second"))
        
        response = client.get("/items/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "success"
        assert len(data["data"]) == 2
        assert data["data"][0]["name"] == "First Item"
        assert data["data"][1]["name"] == "Second Item"

    def test_format_error_returns_standardized_dict(self) -> None:
        """Verifies that format_error utility function returns a standardized dictionary."""
        from utils.helpers import format_error
        result = format_error("Something went wrong")
        assert result == {"status": "error", "message": "Something went wrong"}

