import pandas as pd
import pytest


@pytest.fixture
def movies_df():
    # ARRANGE
    return pd.DataFrame(
        [
            {
                "item_id": 1,
                "title": "Action Movie",
                "genres": "Action|Adventure",
            },
            {
                "item_id": 2,
                "title": "Romance Movie",
                "genres": "Romance|Drama",
            },
            {
                "item_id": 3,
                "title": "Comedy Movie",
                "genres": "Comedy",
            },
        ]
    )