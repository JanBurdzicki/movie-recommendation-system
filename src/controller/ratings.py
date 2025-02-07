from fastapi import APIRouter, Depends, Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from model.utils import get_db
from model.utils import Rating

router = APIRouter()
templates = Jinja2Templates(directory="src/view")


@router.get("/", response_class=HTMLResponse)
async def read_ratings(request: Request):
    return templates.TemplateResponse("add_rating.html", {"request": request})

@router.post("/")
def add_rating(
    movie_id: int = Form(...),
    rating: float = Form(...),
    db: Session = Depends(get_db)
):
    new_rating = Rating(user_id=1, movie_id=movie_id, rating=rating)  # TODO: replace with authenticated user
    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}

@router.get("/user", response_class=HTMLResponse)
def get_user_ratings(request: Request, db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == 1).all()  # TODO: replace with authenticated user
    return templates.TemplateResponse("ratings.html", {"request": request, "ratings": ratings})