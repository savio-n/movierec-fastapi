
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class ContentRecommender:
    REQUIRED_COLUMNS = ("item_id", "title", "genres")

    def __init__(self, movies: pd.DataFrame | None = None):
        if movies is None:
            movies = pd.DataFrame([
                {"item_id": 1, "title": "The Matrix", "genres": "Action Sci-Fi"},
                {"item_id": 2, "title": "Inception", "genres": "Action Sci-Fi Thriller"},
                {"item_id": 3, "title": "The Notebook", "genres": "Romance Drama"},
                {"item_id": 4, "title": "Interstellar", "genres": "Sci-Fi Drama"},
                {"item_id": 5, "title": "Titanic", "genres": "Romance Drama"}
            ])

        self.movies = movies.copy()
        self.users_preferences = {}

        self._prepare_movies()
        self._update_model()

    def _prepare_movies(self):
        missing_columns = set(self.REQUIRED_COLUMNS) - set(self.movies.columns)

        if missing_columns:
            raise ValueError(
                f"Colunas ausentes na base de filmes: {missing_columns}"
            )

        self.movies = self.movies[list(self.REQUIRED_COLUMNS)].copy()

        self.movies["item_id"] = self.movies["item_id"].astype(int)
        self.movies["title"] = self.movies["title"].fillna("").astype(str)

        self.movies["genres"] = (
            self.movies["genres"]
            .fillna("")
            .astype(str)
            .str.replace("|", " ", regex=False)
        )

        self.movies = self.movies.reset_index(drop=True)

        if self.movies.empty:
            raise ValueError("A base de filmes não pode estar vazia.")

        if self.movies["item_id"].duplicated().any():
            raise ValueError("Existem identificadores de filmes duplicados.")

        if self.movies["genres"].str.strip().eq("").all():
            raise ValueError("A base não possui gêneros válidos.")

    def _update_model(self):
        self.tfidf = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.tfidf.fit_transform(
            self.movies["genres"]
        )

    def add_item(self, item_id: int, title: str, genres: list[str]):
        if item_id in self.movies["item_id"].values:
            raise ValueError(f"O filme {item_id} já está cadastrado.")

        genres_str = " ".join(genres)

        new_row = pd.DataFrame([{
            "item_id": item_id,
            "title": title,
            "genres": genres_str
        }])

        self.movies = pd.concat(
            [self.movies, new_row],
            ignore_index=True
        )

        self._prepare_movies()
        self._update_model()

    def set_user_preference(self, user_id: int, genres: list[str]):
        self.users_preferences[user_id] = " ".join(genres)

    def recommend(self, user_id: int, top_n: int = 3):
        if top_n < 1:
            raise ValueError("O limite de recomendações deve ser positivo.")

        query = self.users_preferences.get(
            user_id,
            "Action Sci-Fi"
        )

        user_vec = self.tfidf.transform([query])

        cosine_sim = linear_kernel(
            user_vec,
            self.tfidf_matrix
        ).flatten()

        related_docs_indices = cosine_sim.argsort()[::-1][:top_n]

        recommendations = []

        for idx in related_docs_indices:
            recommendations.append({
                "item_id": int(self.movies.iloc[idx]["item_id"]),
                "title": str(self.movies.iloc[idx]["title"]),
                "score": round(float(cosine_sim[idx]), 4)
            })

        return recommendations
