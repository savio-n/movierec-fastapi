from fastapi import FastAPI
from app.schemas import UserPreference, Item, RecommendationResponse
from app.recommender import ContentRecommender

app = FastAPI(
    title="Sistema de Recomendação de Filmes API",
    description="API com filtragem baseada em conteúdo utilizando FastAPI e Docker.",
    version="1.0.0"
)

recommender = ContentRecommender()

@app.get("/")
def read_root():
    return {"message": "API de Recomendação online. Acesse /docs para Swagger UI."}

@app.post("/items/", status_code=201)
def add_item(item: Item):
    recommender.add_item(item.item_id, item.title, item.genres)
    return {"status": "Item adicionado com sucesso", "item": item}

@app.post("/users/preferences/")
def update_preferences(pref: UserPreference):
    recommender.set_user_preference(pref.user_id, pref.preferred_genres)
    return {"status": "Preferências atualizadas", "user_id": pref.user_id}

@app.get("/recommendations/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: int, limit: int = 3):
    recs = recommender.recommend(user_id=user_id, top_n=limit)
    return {"user_id": user_id, "recommendations": recs}
