from fastapi import FastAPI, Depends, HTTPException, status
from passlib.context import CryptContext
import uvicorn
from pydantic import BaseModel

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

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
