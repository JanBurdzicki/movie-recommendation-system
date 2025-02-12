# Recommendation System project for LLM course

## Prerequisites

Ensure you have the following installed on your system:
* Python 3
* PostgreSQL

## Setting Up the Database

1. Switch to the PostgreSQL user:
   ```sh
   sudo -i -u postgres
   ```
2. Access PostgreSQL:
   ```sh
   psql
   ```
3. Create a new user with superuser privileges:
   ```sql
   CREATE USER username WITH SUPERUSER PASSWORD 'password';
   ```

## Configuring Environment Variables

Create a `.env` file in the root directory and add the following configurations:

```env
DB_NAME = "recommender"
DB_USER = "username"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

Note: Modify `.env` with actual credentials if needed.

## Running the Application
1. Initialize the database:
   ```sh
   python3 src/model/utils.py
   ```
2. Start the application:
   ```sh
   python3 src/main.py
   ```

## Get data
```shell
cd data
PYTHONPATH='.' poetry run python3 data/get_data.py
```

## Use recommendation package
Our code are based on the ollama server. Install ollama from https://ollama.com/download and if server is not started use command `ollama serve`.

### Running as a script
```shell
python -m recommender.recommender
```
(remember to change variables in `recommender/recommender.py`)

### In your code
You can create instance of RecommenderSystem:
```python
from recommender.recommender import RecommenderSystem

# --- #

recommender_system = RecommenderSystem(data_folder="path/to/data")
item = {"title": "Forrest Gump"}
recommender_system.recommend_similar_items(item, 3)
```

or only a EmbeddingModel:
```python
from recommender.embeddings import EmbeddingModel

# --- #

embedding_model = EmbeddingModel()
item = {"title": "Forrest Gump"}
embedding = embedding_model.get_embedding(item)
```

You can also pass many different keys to the item dict, e.g. genre, overview, rating, actors and so on.