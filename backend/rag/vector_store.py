import faiss
import numpy as np
import json
import os
import pickle
from typing import List, Dict, Tuple
from backend.config import config

class VectorStore:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.dimension = 384  # Dimension for all-MiniLM-L6-v2

    def create_index(self, embeddings: np.ndarray, metadata: List[Dict]):
        """
        Creates a new FAISS index from embeddings and stores metadata.
        """
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings)
        self.metadata = metadata
        self.save_index()

    def add_documents(self, embeddings: np.ndarray, metadata: List[Dict]):
        """
        Adds documents to the existing index.
        """
        if self.index is None:
            self.create_index(embeddings, metadata)
        else:
            self.index.add(embeddings)
            self.metadata.extend(metadata)
            self.save_index()

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Searches the index for the k nearest neighbors.
        Returns a list of metadata dicts for the matching chunks.
        """
        if self.index is None or len(self.metadata) == 0:
            return []
        
        # FAISS expects a 2D array for search
        query_vec = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_vec, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                result = self.metadata[idx].copy()
                result['score'] = float(distances[0][i])
                results.append(result)
        
        return results

    def save_index(self):
        """
        Saves the FAISS index and metadata to disk.
        """
        if self.index:
            faiss.write_index(self.index, config.FAISS_INDEX_PATH)
        
        with open(config.METADATA_PATH, 'w') as f:
            json.dump(self.metadata, f)

    def load_index(self):
        """
        Loads the FAISS index and metadata from disk.
        """
        if os.path.exists(config.FAISS_INDEX_PATH) and os.path.exists(config.METADATA_PATH):
            self.index = faiss.read_index(config.FAISS_INDEX_PATH)
            with open(config.METADATA_PATH, 'r') as f:
                self.metadata = json.load(f)
            return True
        return False
