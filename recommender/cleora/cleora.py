import pickle

import numpy as np
import networkx as nx
from scipy.spatial.distance import cosine

from recommender.cleora.graph_creation import create_graph


class Cleora:
    def __init__(self, graph, embedding_dim=128, iterations=3):
        self.graph = graph
        self.embedding_dim = embedding_dim
        self.iterations = iterations
        self.node_list = list(graph.nodes())
        self.node_to_index = {node: i for i, node in enumerate(self.node_list)}
        self.index_to_node = {i: node for node, i in self.node_to_index.items()}

    def initialize_embeddings(self):
        """Initialize one-hot embeddings."""
        num_nodes = len(self.node_list)
        embeddings = np.eye(num_nodes)
        return embeddings

    def compute_embeddings(self):
        """Compute Cleora embeddings iteratively."""
        embeddings = self.initialize_embeddings()
        adjacency_matrix = nx.to_numpy_array(self.graph, nodelist=self.node_list, weight='weight')
        epsilon = 1e-10
        for _ in range(self.iterations):
            embeddings = adjacency_matrix @ embeddings
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True) + epsilon
            embeddings = embeddings / norms

        return {self.index_to_node[i]: embeddings[i] for i in range(len(self.node_list))}


def save_user_embeddings(embeddings: dict, filename: str="user_embeddings.pkl"):
    """Save user embeddings to a file."""
    user_embeddings = {node: emb for node, emb in embeddings.items() if node.startswith("U")}
    with open(filename, "wb") as f:
        pickle.dump(user_embeddings, f)
    print(f"User embeddings saved to {filename}")

def recommend_movies(cleora: Cleora, user_id: int, top_n: int=5, threshold: float=0.5):
    """Recommend movies for a user based on similar users."""
    embeddings = cleora.compute_embeddings()
    user_node = f"U{user_id}"

    if user_node not in embeddings:
        print(f"User {user_node} not found in the database. Trying to find it.")
        return []

    user_embedding = embeddings[user_node]
    similarities = {}
    sims = []
    for other_user in [n for n in cleora.node_list if n.startswith("U") and n != user_node]:
        sim = 1 - cosine(user_embedding, embeddings[other_user])
        sims.append(sim)
        if sim >= threshold:
            similarities[other_user] = sim

    similar_users = sorted(similarities, key=similarities.get, reverse=True)[:5]

    recommended_movies = set()
    user_movies = set(nx.neighbors(cleora.graph, user_node))

    for similar_user in similar_users:
        similar_user_movies = set(nx.neighbors(cleora.graph, similar_user))
        recommended_movies.update(similar_user_movies - user_movies)

    return [cleora.node_to_index[movie] for movie in list(recommended_movies)[:top_n]]


def get_watched_movies(session, user_id):
    """Fetch movies a user has watched along with their ratings."""
    from src.model.utils import Rating, Movie  # Ensure correct import paths

    watched_movies = (
        session.query(Movie.title, Rating.rating)
        .join(Rating, Rating.movie_id == Movie.id)
        .filter(Rating.user_id == user_id)
        .all()
    )
    return watched_movies


if __name__ == '__main__':
    graph = create_graph()

    cleora = Cleora(graph, embedding_dim=128, iterations=11)
    embeddings = cleora.compute_embeddings()

    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    from src.model.utils import Movie

    save_user_embeddings(embeddings, "user_embeddings.pkl")

    DATABASE_URL = "postgresql://username:password@localhost/recommender"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    for i in range(1, 2):
        i = 30
        watched_movies = get_watched_movies(session, user_id=i)
        recommended_movies_ids = recommend_movies(cleora, user_id=i, top_n=8)

        movies = session.query(Movie).all()
        recommended_movies = [str(movie.title) for movie in movies if movie.id in recommended_movies_ids]

        if watched_movies or recommended_movies:
            print(f"\nUser {i} Watched Movies, Ratings, and Recommendations:")

            # Zip the lists to align them in columns
            max_len = max(len(watched_movies), len(recommended_movies))
            watched_movies_padded = watched_movies + [("", "")] * (max_len - len(watched_movies))
            recommended_movies_padded = recommended_movies + [""] * (max_len - len(recommended_movies))

            print("\n{:<40} {:<10} {:<40}".format("Watched Movie", "Rating", "Recommended Movie"))
            print("-" * 90)

            for (watched, rating), recommended in zip(watched_movies_padded, recommended_movies_padded):
                print("{:<40} {:<10} {:<40}".format(watched, rating, recommended))
