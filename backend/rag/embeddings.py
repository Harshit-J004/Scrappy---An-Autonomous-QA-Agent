from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from backend.config import config

class EmbeddingGenerator:
    def __init__(self):
        # Load the model. This might take a moment on first run to download.
        print(f"Loading embedding model: {config.EMBEDDING_MODEL}...")
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        print("Embedding model loaded.")

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generates embeddings for a list of texts.
        Returns a numpy array of embeddings.
        """
        if not texts:
            return np.array([])
        
        embeddings = self.model.encode(texts)
        return embeddings

    def generate_query_embedding(self, query: str) -> np.ndarray:
        """
        Generates embedding for a single query string.
        """
        return self.model.encode([query])[0]
