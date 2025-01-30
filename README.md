# Recommendation System project for LLM course

## Get data
```shell
cd data
PYTHONPATH='.' poetry run python3 data/get_data.py
```

## Use recommendation package
### Running as a script
```shell
python -m recommender.recommender
```

### In your code
You can create instance of RecommenderSystem:
```python
from recommender.recommender import RecommenderSystem

# --- #

recommender_system = RecommenderSystem(data_folder="path/to/data")
item = {"title": "Forrest Gump"}
recommender_system.recommend_similar_items(item, 3)
```

Or just an EmbeddingModel:
```python
from recommender.embeddings import EmbeddingModel

# --- #

embedding_model = EmbeddingModel()
item = {"title": "Forrest Gump"}
embedding = embedding_model.get_embedding(item)
```

You can also pass many different keys to the item dict, e.g. genre, overview, rating, actors and so on.