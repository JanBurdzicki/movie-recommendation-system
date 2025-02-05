from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from model.tables import SessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/")
# def add_rating(rating: RatingSchema, db: Session = Depends(get_db)):
#     new_rating = Rating(user_id=1, movie_id=rating.movie_id, rating=rating.rating)  # TODO: replace with authenticated user
#     db.add(new_rating)
#     db.commit()
#     return {"message": "Rating added successfully"}

# @router.get("/user")
# def get_user_ratings(db: Session = Depends(get_db)):
#     ratings = db.query(Rating).filter(Rating.user_id == 1).all()  # TODO: replace with authenticated user
#     return ratings