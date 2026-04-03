import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database import db


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
async def test_db():
    """Setup test database."""
    await db.connect()
    yield db
    await db.disconnect()
