import os

import numpy as np
from sklearn.neighbors import NearestNeighbors

from recommender.embeddings import EmbeddingModel


class RecommenderSystem:
    def __init__(
        self,
        data_folder: str,
        model_name: str = "snowflake-arctic-embed",
        num_neighbors: int = 5,
    ):
        """
        Initializes the recommender system with an embedding model and KNN.

        Args:
            data_folder (str): The folder where embeddings are stored.
            num_neighbors (int): Number of similar items to return.
        """
        self.embedding_model = EmbeddingModel(model=model_name)
        self.item_embeddings = {}
        self.data_folder = os.path.join(data_folder, model_name)
        self.num_neighbors = num_neighbors
        self.model_name = model_name

        self.knn_model = None
        self.embeddings_matrix = None
        self.titles = []

        os.makedirs(self.data_folder, exist_ok=True)
        self.restore_embeddings()

    def save_embedding(self, title: str, embedding: np.ndarray):
        """
        Saves the embedding for a given item as a .npy file.

        Args:
            title (str): Movie title of embedding to be saved.
            embedding (np.ndarray): The embedding vector.
        """
        file_path = os.path.join(self.data_folder, f"{title.replace(' ', '_')}.npy")
        np.save(file_path, embedding)

    def restore_embeddings(self):
        """
        Loads all stored embeddings from the data folder and initializes the KNN model.
        """
        for file_name in os.listdir(self.data_folder):
            if file_name.endswith(".npy"):
                file_path = os.path.join(self.data_folder, file_name)
                title = file_name.replace(".npy", "").replace("_", " ")
                self.item_embeddings[title] = np.load(file_path)

        if self.item_embeddings:
            self._train_knn_model()

    def _train_knn_model(self):
        """
        Trains the KNN model using the stored embeddings.
        """
        self.titles = list(self.item_embeddings.keys())
        self.embeddings_matrix = np.array(list(self.item_embeddings.values()))

        if len(self.titles) > 1:
            self.knn_model = NearestNeighbors(
                n_neighbors=self.num_neighbors, metric="cosine"
            )
            self.knn_model.fit(self.embeddings_matrix)

    def recommend_similar_items(self, target_item: dict, num_recommendations: int = 5):
        """
        Recommends similar items based on KNN similarity.

        Args:
            target_item (dict): The item details (e.g., title, genre, overview).
            num_recommendations (int): Number of recommendations to return.

        Returns:
            list: List of recommended items.
        """
        title = target_item["title"]

        if title in self.item_embeddings:
            target_embedding = self.item_embeddings[title]
        else:
            target_embedding = self.embedding_model.get_embedding(target_item)
            self.item_embeddings[title] = target_embedding
            self.save_embedding(title, target_embedding)
            self._train_knn_model()

        recommended_titles = []
        if self.knn_model is not None:
            distances, indices = self.knn_model.kneighbors(
                [target_embedding], n_neighbors=num_recommendations
            )
            recommended_titles = [
                self.titles[idx] for idx in indices[0] if self.titles[idx] != title
            ]

        return recommended_titles


if __name__ == "__main__":
    recommender = RecommenderSystem(
        data_folder="data/embeddings", model_name="snowflake-arctic-embed"
    )

    sample_movie = {
        "title": "Inception",
        "genre": "Sci-Fi, Thriller",
        "overview": "A thief who enters the dreams of others...",
    }

    recommendations = recommender.recommend_similar_items(sample_movie)
    print("Recommended movies:", recommendations)
