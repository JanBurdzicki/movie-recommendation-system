import networkx as nx
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.model.utils import User, Movie, Rating


def create_graph():
    DATABASE_URL = "postgresql://username:password@localhost/recommender"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    users = session.query(User).all()
    movies = session.query(Movie).all()
    ratings = session.query(Rating).all()

    graph = nx.Graph()
    for user in users:
        graph.add_node(f"U{user.id}", bipartite=0)
    for movie in movies:
        graph.add_node(f"M{movie.id}", bipartite=1)
    for rating in ratings:
        graph.add_edge(f"U{rating.user_id}", f"M{rating.movie_id}", weight=rating.rating)

    return graph
