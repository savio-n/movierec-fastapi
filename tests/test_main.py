from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"].startswith("API de Recomendação")

def test_add_item():
    payload = {"item_id": 99, "title": "Avatar", "genres": ["Action", "Sci-Fi"]}
    response = client.post("/items/", json=payload)
    assert response.status_code == 201

def test_recommendations():
    response = client.get("/recommendations/1")
    assert response.status_code == 200
    assert "recommendations" in response.json()
