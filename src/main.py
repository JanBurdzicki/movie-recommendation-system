from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
import uvicorn
from pydantic import BaseModel

from controller.main import router as main_router
from controller.movies import router as movies_router
from controller.ratings import router as ratings_router
from controller.recommendations import router as recommendations_router
from controller.users import router as users_router

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.include_router(main_router, prefix="")
app.include_router(movies_router, prefix="/movies")
app.include_router(ratings_router, prefix="/ratings")
app.include_router(recommendations_router, prefix="/recommendations")
app.include_router(users_router, prefix="/users")

# schemas
class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MovieSchema(BaseModel):
    id: int
    title: str
    genre: str
    genre: str
    overview: str
    rating: float
    director: str
    actors: str

class RatingSchema(BaseModel):
    movie_id: int
    rating: float

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
