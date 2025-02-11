from fastapi import APIRouter, HTTPException, Form
from fastapi.templating import Jinja2Templates

from recommender.recommender import RecommenderSystem


router = APIRouter()
templates = Jinja2Templates(directory="src/view")
recommender = RecommenderSystem(
    data_folder="data/embeddings", model_name="snowflake-arctic-embed"
)

@router.get("/user")
async def get_user_recommendations():
    return {"message": "User recommendations"}

@router.post("/movie")
async def get_movie_recommendations(
    title: str = Form(...),
    description: str = Form(...),
    genre: str = Form(...)
):
    try:
        print(len(recommender.item_embeddings))
        recommendations = recommender.recommend_similar_items({"title": title, "description": description, "genre": genre})
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
