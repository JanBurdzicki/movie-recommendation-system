from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from model.utils import Database

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

@router.get("/{movie_id}", response_class=HTMLResponse)
async def get_movie(request: Request, movie_id: int, db: Session = Depends(Database.get_db)):
    # movie = db.query(Movie).filter(Movie.id == movie_id).first()
    # if not movie:
        # raise HTTPException(status_code=404, detail="Movie not found")
    # return movie
    return templates.TemplateResponse("movie.html", {"request": request, "movie": movie_id})

@router.get("/search", response_class=HTMLResponse)
async def search_movies(request: Request, query: str, db: Session = Depends(Database.get_db)):
    # movies = db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).all()
    # return movies
    return templates.TemplateResponse("search_results.html", {"request": request})
