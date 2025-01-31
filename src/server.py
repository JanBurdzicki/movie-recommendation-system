from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from passlib.context import CryptContext
import uvicorn
from pydantic import BaseModel

# database setup
DATABASE_URL = "postgresql://username:password@localhost/recommender"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)

    user = relationship("User")
    movie = relationship("Movie")

Base.metadata.create_all(bind=engine)

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

class RatingSchema(BaseModel):
    movie_id: int
    rating: float

# routes
@app.get("/")
def home():
    return {"message": "Welcome to the Movie Recommender System"}

@app.post("/users/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/users/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.get("/movies/search")
def search_movies(query: str, db: Session = Depends(get_db)):
    movies = db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).all()
    return movies

@app.post("/ratings")
def add_rating(rating: RatingSchema, db: Session = Depends(get_db)):
    new_rating = Rating(user_id=1, movie_id=rating.movie_id, rating=rating.rating)  # TODO: replace with authenticated user
    db.add(new_rating)
    db.commit()
    return {"message": "Rating added successfully"}

@app.get("/ratings/user")
def get_user_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).filter(Rating.user_id == 1).all()  # TODO: replace with authenticated user
    return ratings

@app.get("/recommendations/user")
def get_user_recommendations():
    return {"message": "User recommendations"}

@app.get("/recommendations/movie/{movie_id}")
def get_movie_recommendations(movie_id: int):
    return {"message": f"Recommendations for movie {movie_id}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
