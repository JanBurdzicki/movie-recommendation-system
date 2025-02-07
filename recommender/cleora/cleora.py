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
        return []

    user_embedding = embeddings[user_node]
    similarities = {}

    for other_user in [n for n in cleora.node_list if n.startswith("U") and n != user_node]:
        sim = 1 - cosine(user_embedding, embeddings[other_user])
        if sim >= threshold:
            similarities[other_user] = sim

    similar_users = sorted(similarities, key=similarities.get, reverse=True)[:5]

    recommended_movies = set()
    user_movies = set(nx.neighbors(cleora.graph, user_node))

    for similar_user in similar_users:
        similar_user_movies = set(nx.neighbors(cleora.graph, similar_user))
        recommended_movies.update(similar_user_movies - user_movies)

    return list(recommended_movies)[:top_n]

if __name__ == '__main__':
    graph = create_graph()

    cleora = Cleora(graph, embedding_dim=128, iterations=23)
    embeddings = cleora.compute_embeddings()

    save_user_embeddings(embeddings, "user_embeddings.pkl")
    for i in range(101, 110):
        recommended_movies = recommend_movies(cleora, user_id=i, top_n=8)
        print(i, ":", recommended_movies)