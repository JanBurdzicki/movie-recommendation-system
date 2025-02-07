from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from model.utils import Database
from model.utils import RatingSchema

router = APIRouter()
templates = Jinja2Templates(directory="src/view")


@router.post("/")
def add_rating(rating: RatingSchema, db: Session = Depends(Database.get_db)):
    new_rating = Rating(user_id=1, movie_id=rating.movie_id, rating=rating.rating)  # TODO: replace with authenticated user
    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}

@router.get("/user")
def get_user_ratings(db: Session = Depends(Database.get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == 1).all()  # TODO: replace with authenticated user
    return ratings