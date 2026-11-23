import pytest

from app.recommender import ContentRecommender


@pytest.fixture
def recommender(movies_df):
    return ContentRecommender(movies_df)