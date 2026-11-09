from pydantic import BaseModel
from typing import List

class UserPreference(BaseModel):
    user_id: int
    preferred_genres: List[str]

class Item(BaseModel):
    item_id: int
    title: str
    genres: List[str]

class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[dict]
