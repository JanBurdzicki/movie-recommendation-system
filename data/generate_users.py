import random

import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from src.models import Movie, Rating, User

if __name__ == "__main__":
    DATABASE_URL = "postgresql://username:password@localhost/recommender"
    engine = create_engine(DATABASE_URL)
    session = Session(bind=engine)

    users = session.query(User).all()
    movies = session.query(Movie).all()
    ratings_per_user = random.randint(7, 12)

    for user in users:
        rated_movies = random.sample(movies, min(ratings_per_user, len(movies)))
        for movie in rated_movies:
            avg_movie_rating = movie.rating if movie.rating is not None else 5.0
            noise = random.uniform(-1.5, 1.5)
            rating_value = round(max(1, min(10, avg_movie_rating + noise)), 1)
            rating = Rating(user_id=user.id, movie_id=movie.id, rating=rating_value)
            session.add(rating)

    session.commit()
    session.close()
