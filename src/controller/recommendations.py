from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

@router.get("/user")
async def get_user_recommendations():
    return {"message": "User recommendations"}

@router.get("/movie/{movie_id}")
async def get_movie_recommendations(movie_id: int):
    return {"message": f"Recommendations for movie {movie_id}"}
