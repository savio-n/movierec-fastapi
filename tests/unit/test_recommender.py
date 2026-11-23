"""Testes unitários do algoritmo de recomendação."""

import pandas as pd
import pytest

from app.recommender import ContentRecommender


def test_recommendation_matches_user_genres(recommender):
    # ARRANGE
    recommender.set_user_preference(123, ["Romance", "Drama"])

    # ACT
    recommendations = recommender.recommend(user_id=123, top_n=2)

    # ASSERT
    assert len(recommendations) == 2
    assert recommendations[0]["item_id"] == 2
    assert recommendations[0]["score"] > 0


def test_recommendation_uses_default_preferences(recommender):
    # ARRANGE
    new_user_id = 555

    # ACT
    recommendations = recommender.recommend(new_user_id, top_n=1)

    # ASSERT
    assert recommendations[0]["item_id"] == 1


@pytest.mark.parametrize("limit", [0, -1, -10])
def test_recommendation_rejects_invalid_limit(recommender, limit):
    # ARRANGE
    user_id = 123

    # ACT / ASSERT
    with pytest.raises(ValueError, match="positivo"):
        recommender.recommend(user_id=user_id, top_n=limit)


def test_add_item_updates_catalog_and_model(recommender):
    # ARRANGE
    initial_count = len(recommender.movies)
    new_id = 99

    # ACT
    recommender.add_item(new_id, "New Film", ["Fantasy", "Adventure"])
    recommender.set_user_preference(123, ["Fantasy", "Adventure"])
    recommendations = recommender.recommend(123, top_n=1)

    # ASSERT
    assert len(recommender.movies) == initial_count + 1
    assert recommender.tfidf_matrix.shape[0] == initial_count + 1
    assert recommendations[0]["item_id"] == new_id


def test_add_item_rejects_duplicate_id(recommender):
    # ARRANGE
    existing_id = 1

    # ACT / ASSERT
    with pytest.raises(ValueError, match="já está cadastrado"):
        recommender.add_item(existing_id, "Duplicate Film", ["Action"])


def test_catalog_rejects_duplicate_ids(movies_df):
    # ARRANGE
    duplicated_catalog = pd.concat([movies_df, movies_df.iloc[[0]]], ignore_index=True)

    # ACT / ASSERT
    with pytest.raises(ValueError, match="duplicados"):
        ContentRecommender(duplicated_catalog)


def test_catalog_rejects_missing_columns(movies_df):
    # ARRANGE
    invalid_catalog = movies_df.drop(columns=["genres"])

    # ACT / ASSERT
    with pytest.raises(ValueError, match="Colunas ausentes"):
        ContentRecommender(invalid_catalog)


def test_catalog_rejects_empty_dataframe(movies_df):
    # ARRANGE
    empty_catalog = movies_df.iloc[0:0].copy()

    # ACT / ASSERT
    with pytest.raises(ValueError, match="não pode estar vazia"):
        ContentRecommender(empty_catalog)
