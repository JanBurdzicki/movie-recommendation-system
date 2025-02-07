import random
import string

import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.model.utils import Movie, Rating, User


def generate_random_username(length=8):
    """Generate a random username."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def create_dummy_users(n=10, session=None):
    """Create and insert dummy users into the database."""
    for _ in range(n):
        username = generate_random_username()
        password_hash = "pass123"

        user = User(username=username, password_hash=password_hash)
        session.add(user)

        try:
            session.commit()
            print(f"User {username} created successfully.")
        except IntegrityError:
            session.rollback()
            print(f"Username {username} already exists. Skipping.")


def create_movies_from_csv(csv_path):
    """Create and insert movies from a CSV file into the database."""
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        movie = Movie(
            title=row.get("Series_Title", "Unknown"),
            genre=row.get("Genre", "Unknown"),
            overview=row.get("Overview", ""),
            rating=row.get("IMDB Rating", 5.0),
            director=row.get("Director", "Unknown"),
            actors=row.get("Actors", "Unknown")
        )
        session.add(movie)

    try:
        session.commit()
        print("Movies inserted successfully.")
    except IntegrityError:
        session.rollback()
        print("Error inserting movies. Some might already exist.")


if __name__ == "__main__":
    DATABASE_URL = "postgresql://username:password@localhost/recommender"
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine)

    create_dummy_users(50, session)
    create_movies_from_csv("/home/kabanosk/.cache/kagglehub/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows/versions/1/imdb_top_1000.csv")
    users = session.query(User).all()
    movies = session.query(Movie).all()
    ratings_per_user = random.randint(7, 12)

    for user in users:
        rated_movies = random.sample(movies, min(ratings_per_user, len(movies)))
        for movie in rated_movies:
            avg_movie_rating = movie.rating if movie.rating is not None else 5.0
            noise = random.uniform(-1, 2)
            rating_value = round(max(1, min(10, avg_movie_rating + noise)), 1)
            rating = Rating(user_id=user.id, movie_id=movie.id, rating=rating_value)
            session.add(rating)

    session.commit()
    session.close()
