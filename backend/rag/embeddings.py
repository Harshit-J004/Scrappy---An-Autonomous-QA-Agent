from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
import os
import google.generativeai as genai
from backend.config import config

class EmbeddingGenerator:
    def __init__(self):
        self.is_render = os.getenv("RENDER") == "true"
        
        if self.is_render:
            print("🚀 Running on Render: Using Gemini API Embeddings (Lightweight)")
            genai.configure(api_key=config.GOOGLE_API_KEY)
        else:
            print(f"💻 Running Locally: Loading {config.EMBEDDING_MODEL}...")
            self.model = SentenceTransformer(config.EMBEDDING_MODEL)
            print("Embedding model loaded.")

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        
        if self.is_render:
            # Gemini API Embedding
            try:
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=texts,
                    task_type="retrieval_document"
                )
                return np.array(result['embedding'])
            except Exception as e:
                print(f"Gemini Embedding Error: {e}")
                return np.array([])
        else:
            # Local SentenceTransformer
            return self.model.encode(texts)

    def generate_query_embedding(self, query: str) -> np.ndarray:
        if self.is_render:
            try:
                result = genai.embed_content(
                    model="models/text-embedding-004",
                    content=query,
                    task_type="retrieval_query"
                )
                return np.array(result['embedding'])
            except Exception as e:
                print(f"Gemini Embedding Error: {e}")
                return np.array([])
        else:
            return self.model.encode([query])[0]
