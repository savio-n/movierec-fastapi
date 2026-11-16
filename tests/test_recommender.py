
import pandas as pd
import pytest

from app.recommender import ContentRecommender


def test_recommender_accepts_external_dataframe():
    movies = pd.DataFrame([
        {"item_id": 1, "title": "The Matrix", "genres": "Action|Sci-Fi"},
        {"item_id": 2, "title": "The Notebook", "genres": "Romance|Drama"},
    ])

    recommender = ContentRecommender(movies)

    assert len(recommender.movies) == 2
    assert recommender.movies.iloc[0]["title"] == "The Matrix"
    assert " " in recommender.movies.iloc[0]["genres"]


def test_recommender_rejects_missing_columns():
    movies = pd.DataFrame([
        {"item_id": 1, "title": "The Matrix"}
    ])

    with pytest.raises(ValueError):
        ContentRecommender(movies)


def test_recommender_rejects_duplicate_ids():
    movies = pd.DataFrame([
        {"item_id": 1, "title": "The Matrix", "genres": "Action"},
        {"item_id": 1, "title": "Another Movie", "genres": "Drama"},
    ])

    with pytest.raises(ValueError):
        ContentRecommender(movies)


def test_recommender_rejects_empty_dataset():
    movies = pd.DataFrame(columns=["item_id", "title", "genres"])

    with pytest.raises(ValueError):
        ContentRecommender(movies)


def test_recommendation_limit():
    recommender = ContentRecommender()

    recommendations = recommender.recommend(user_id=1, top_n=2)

    assert len(recommendations) == 2


def test_recommendation_rejects_invalid_limit():
    recommender = ContentRecommender()

    with pytest.raises(ValueError):
        recommender.recommend(user_id=1, top_n=0)
