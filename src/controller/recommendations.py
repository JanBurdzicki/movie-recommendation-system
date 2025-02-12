from fastapi import APIRouter, Form, HTTPException
from fastapi.templating import Jinja2Templates

from recommender.cleora.cleora import Cleora
from recommender.cleora.graph_creation import create_graph
from recommender.recommender import RecommenderSystem
from src.model.utils import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="src/view")
recommender = RecommenderSystem(
    data_folder="data/embeddings", model_name="snowflake-arctic-embed"
)


@router.get("/user")
async def get_user_recommendations():
    graph = create_graph()
    cleora = Cleora(graph, embedding_dim=128, iterations=11)
    recommended_movies = cleora.recommend_movies(user_id=get_current_user())

    return {"message": "User recommendations"}


@router.post("/movie")
async def get_movie_recommendations(
    title: str = Form(...), description: str = Form(...), genre: str = Form(...)
):
    try:
        recommendations = recommender.recommend_similar_items(
            {"title": title, "description": description, "genre": genre}
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
