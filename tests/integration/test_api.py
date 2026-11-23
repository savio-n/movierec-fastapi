"""Testes dos contratos HTTP da aplicação."""


def test_read_root(client):
    # ARRANGE
    endpoint = "/"

    # ACT
    response = client.get(endpoint)

    # ASSERT
    assert response.status_code == 200
    assert response.json()["message"].startswith("API de Recomendação")


def test_healthcheck(client):
    # ARRANGE
    endpoint = "/health"

    # ACT
    response = client.get(endpoint)

    # ASSERT
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_add_item(client, recommender):
    # ARRANGE
    payload = {"item_id": 99, "title": "New Film", "genres": ["Action", "Sci-Fi"]}
    initial_count = len(recommender.movies)

    # ACT
    response = client.post("/items/", json=payload)

    # ASSERT
    assert response.status_code == 201
    assert response.json()["item"] == payload
    assert len(recommender.movies) == initial_count + 1
    assert 99 in recommender.movies["item_id"].values


def test_add_item_invalid_payload(client):
    # ARRANGE
    payload = {"item_id": "not-an-int", "title": "Invalid", "genres": ["Action"]}

    # ACT
    response = client.post("/items/", json=payload)

    # ASSERT
    assert response.status_code == 422


def test_update_user_preferences(client, recommender):
    # ARRANGE
    payload = {"user_id": 123, "preferred_genres": ["Romance", "Drama"]}

    # ACT
    response = client.post("/users/preferences/", json=payload)

    # ASSERT
    assert response.status_code == 200
    assert response.json()["user_id"] == 123
    assert recommender.users_preferences[123] == "Romance Drama"


def test_recommendations(client):
    # ARRANGE
    user_id = 123
    payload = {"user_id": user_id, "preferred_genres": ["Romance", "Drama"]}
    client.post("/users/preferences/", json=payload)

    # ACT
    response = client.get(f"/recommendations/{user_id}?limit=2")

    # ASSERT
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == user_id
    assert len(body["recommendations"]) == 2
    assert body["recommendations"][0]["item_id"] == 2
    assert all({"item_id", "title", "score"} <= item.keys() for item in body["recommendations"])


def test_recommendations_invalid_user_id(client):
    # ARRANGE
    endpoint = "/recommendations/not-an-integer"

    # ACT
    response = client.get(endpoint)

    # ASSERT
    assert response.status_code == 422
