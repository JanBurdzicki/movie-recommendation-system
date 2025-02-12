from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.model.utils import Rating, get_current_user, get_db

router = APIRouter()
templates = Jinja2Templates(directory="src/view")


@router.get("/", response_class=HTMLResponse)
async def read_ratings(request: Request):
    return templates.TemplateResponse("add_rating.html", {"request": request})


@router.post("/")
def add_rating(
    movie_id: int = Form(...), rating: float = Form(...), db: Session = Depends(get_db)
):
    user_id = get_current_user()
    if user_id == None:
        raise HTTPException(status_code=400, detail=f"User is not logged in")

    new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}


@router.get("/user/{user_id}", response_class=HTMLResponse)
def get_user_ratings(request: Request, user_id: int, db: Session = Depends(get_db)):
    # user_id = get_current_user()
    # if user_id == None:
    # raise HTTPException(status_code=400, detail=f"User is not logged in")

    ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    return templates.TemplateResponse(
        "ratings.html", {"request": request, "ratings": ratings}
    )
