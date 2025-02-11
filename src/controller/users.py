from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from recommender.cleora.cleora import Cleora
from recommender.cleora.graph_creation import create_graph
from src.model.utils import (Movie, User, get_current_user, get_db,
                             set_current_user)

router = APIRouter()
templates = Jinja2Templates(directory="src/view")

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/me", response_class=HTMLResponse)
async def read_user_me(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user()
    graph = create_graph()
    cleora = Cleora(graph, embedding_dim=128, iterations=11)
    recommended_movies = cleora.recommend_movies(user_id=user_id)

    recommended_movies = db.query(Movie).filter(Movie.id.in_(recommended_movies)).all()
    return templates.TemplateResponse(
        "user_me.html",
        {
            "request": request,
            "user_id": user_id,
            "recommended_movies": [movie for movie in recommended_movies],
        },
    )


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Username '{username}' already taken"
        )

    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {f"message": "User '{username}' registered successfully"}

    # return templates.TemplateResponse("register_success.html", {"request": request, "user": user})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user or not pwd_context.verify(password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
        # return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    set_current_user(db_user.id)

    return {"message": "Login successful"}
    # return templates.TemplateResponse("dashboard.html", {"request": request, "user": db_user})
