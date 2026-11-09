import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentRecommender:
    def __init__(self):
        # Base inicial de filmes
        self.movies = pd.DataFrame([
            {"item_id": 1, "title": "The Matrix", "genres": "Action Sci-Fi"},
            {"item_id": 2, "title": "Inception", "genres": "Action Sci-Fi Thriller"},
            {"item_id": 3, "title": "The Notebook", "genres": "Romance Drama"},
            {"item_id": 4, "title": "Interstellar", "genres": "Sci-Fi Drama"},
            {"item_id": 5, "title": "Titanic", "genres": "Romance Drama"}
        ])
        self.users_preferences = {}
        self._update_model()

    def _update_model(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.movies['genres'])

    def add_item(self, item_id: int, title: str, genres: list[str]):
        genres_str = " ".join(genres)
        new_row = pd.DataFrame([{"item_id": item_id, "title": title, "genres": genres_str}])
        self.movies = pd.concat([self.movies, new_row], ignore_index=True)
        self._update_model()

    def set_user_preference(self, user_id: int, genres: list[str]):
        self.users_preferences[user_id] = " ".join(genres)

    def recommend(self, user_id: int, top_n: int = 3):
        if user_id in self.users_preferences:
            query = self.users_preferences[user_id]
        else:
            query = "Action Sci-Fi"  # fallback default

        user_vec = self.tfidf.transform([query])
        cosine_sim = linear_kernel(user_vec, self.tfidf_matrix).flatten()
        related_docs_indices = cosine_sim.argsort()[:-top_n-1:-1]

        recommendations = []
        for idx in related_docs_indices:
            recommendations.append({
                "item_id": int(self.movies.iloc[idx]['item_id']),
                "title": str(self.movies.iloc[idx]['title']),
                "score": round(float(cosine_sim[idx]), 4)
            })
        return recommendations
