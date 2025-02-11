from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.model.utils import Movie, get_db
from recommender.recommender import RecommenderSystem

router = APIRouter()
templates = Jinja2Templates(directory="src/view")


@router.get("/{movie_id}", response_class=HTMLResponse)
async def get_movie(request: Request, movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    recommender = RecommenderSystem(
        data_folder="data/embeddings", model_name="snowflake-arctic-embed"
    )
    recommendations = recommender.recommend_similar_items(
        {
            "id": movie.id,
            "title": movie.title,
            "genre": movie.genre,
            "overview": movie.overview,
            "rating": movie.rating,
            "director": movie.director,
            "actors": movie.actors,
            "poster_link": movie.poster_link,
            "year": movie.year,
        }
    )
    recommended_movies = (
        db.query(Movie)
        .filter(Movie.id.in_([int(movie_id) for movie_id in recommendations]))
        .all()
    )

    return templates.TemplateResponse(
        "movie.html",
        {"request": request, "movie": movie, "recommended_movies": recommended_movies},
    )


@router.get("/search", response_class=HTMLResponse)
async def read_search(request: Request):
    return templates.TemplateResponse("search_results.html", {"request": request})


@router.post("/search")
async def search_movies(
    request: Request, query: str = Form(...), db: Session = Depends(get_db)
):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).all()
    return templates.TemplateResponse(
        "search_results.html", {"request": request, "movies": movies}
    )
