import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client(monkeypatch, recommender):
    # ARRANGE
    monkeypatch.setattr(
        "app.main.recommender",
        recommender,
    )

    with TestClient(app) as test_client:
        yield test_client