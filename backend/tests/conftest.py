from collections.abc import Iterator

import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    """Fixture providing a FastAPI TestClient instance."""
    with TestClient(app) as test_client:
        yield test_client
