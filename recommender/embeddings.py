import json

import numpy as np
import requests


class EmbeddingModel:
    def __init__(
        self,
        top_k=5,
        top_p=0.9,
        ollama_url="http://localhost:11434/api/embeddings",
        model="snowflake-arctic-embed",
    ):
        """
        Initializes the embedding model with parameters.

        Args:
            top_k (int): The number of top recommendations to return.
            top_p (float): The cumulative probability threshold for nucleus sampling.
            ollama_url (str): The URL of the Ollama API endpoint.
            model (str): The model to use for generating embeddings.
        """
        self.top_k = top_k
        self.top_p = top_p
        self.ollama_url = ollama_url
        self.model = model

    def get_embedding(self, query: dict):
        """
        Generates an embedding for the input query using the Ollama API.

        Args:
            query (dict): A dictionary containing relevant movie details (title, genre, actors, etc.).

        Returns:
            np.array: A numerical representation (embedding) of the input query.
        """
        payload = {"model": self.model, "prompt": json.dumps(query)}

        response = requests.post(self.ollama_url, json=payload)

        if response.status_code == 200:
            return np.array(response.json().get("embedding", []))
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    model = EmbeddingModel()
    sample_query = {
        "title": "Inception",
        "genre": "Sci-Fi, Thriller",
        "overview": "A thief who enters the dreams of others...",
    }
    embedding = model.get_embedding(sample_query)
    print(embedding)
