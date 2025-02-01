import os

import kagglehub
import numpy as np
import pandas as pd
from tqdm import tqdm

from recommender.embeddings import EmbeddingModel


def download_and_process_csv(output_folder: str, model: str):
    """
    Downloads the IMDB dataset from KaggleHub, extracts relevant columns,
    generates embeddings, and saves them as .npy files.

    Args:
        output_folder (str): Folder where embeddings will be saved.
        model (str): Name of model to use.
    """
    path = kagglehub.dataset_download(
        "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"
    )
    print("Path to dataset files:", path)

    csv_path = os.path.join(path, model, "imdb_top_1000.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError("CSV file not found in the downloaded dataset.")

    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[
        [
            "Series_Title",
            "Genre",
            "IMDB_Rating",
            "Overview",
            "Director",
            "Star1",
            "Star2",
            "Star3",
            "Star4",
        ]
    ]

    embedding_model = EmbeddingModel(model=model)

    for _, row in tqdm(df.iterrows(), total=len(df)):
        movie_data = {
            "title": row["Series_Title"],
            "genre": row["Genre"],
            "overview": row["Overview"],
            "rating": row["IMDB_Rating"],
            "director": row["Director"],
            "actors": [row["Star1"], row["Star2"], row["Star3"], row["Star4"]],
        }

        embedding = embedding_model.get_embedding(movie_data)
        file_name = f"{row['Series_Title'].replace(' ', '_').replace('/', '')}.npy"
        file_path = os.path.join(output_folder, file_name)
        np.save(file_path, embedding)

    print("Embeddings saved successfully!")


if __name__ == "__main__":
    model_name = "snowflake-arctic-embed"
    download_and_process_csv(output_folder=f"data/embeddings/", model=model_name)
