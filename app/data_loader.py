
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATASET_PATH = BASE_DIR / "data" / "ml-latest-small" / "movies.csv"


def load_movies(dataset_path: str | Path = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    """
    Carrega e prepara os filmes do MovieLens Latest Small.

    Retorna um DataFrame com as colunas:
    item_id, title e genres.
    """
    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Arquivo de filmes não encontrado: {dataset_path}"
        )

    movies = pd.read_csv(dataset_path)

    required_columns = {"movieId", "title", "genres"}
    missing_columns = required_columns - set(movies.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas ausentes no MovieLens: {missing_columns}"
        )

    movies = movies[["movieId", "title", "genres"]].copy()

    movies = movies.rename(columns={"movieId": "item_id"})

    movies["item_id"] = movies["item_id"].astype(int)
    movies["title"] = movies["title"].fillna("").astype(str)
    movies["genres"] = (
        movies["genres"]
        .fillna("")
        .astype(str)
        .str.replace("|", " ", regex=False)
    )

    return movies.reset_index(drop=True)
