# backend/query_handler.py
import openai
from qdrant_client import QdrantClient
from . import config

# This module will be imported by the Streamlit app
# It's better to initialize clients once in the app using caching

def get_clients():
    """Initializes and returns the Qdrant and OpenAI clients."""
    qdrant_client = QdrantClient(path=config.QDRANT_DB_PATH)
    openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    return qdrant_client, openai_client

def search_documents(query: str, qdrant_client: QdrantClient, openai_client: openai.OpenAI, limit: int = 5):
    """
    Searches for documents in Qdrant based on a text query.
    """
    # 1. Get query embedding
    response = openai_client.embeddings.create(
        input=query,
        model=config.EMBEDDING_MODEL
    )
    query_embedding = response.data[0].embedding

    # 2. Search Qdrant
    search_results = qdrant_client.search(
        collection_name=config.QDRANT_COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit,
        with_payload=True
    )
    
    return search_results