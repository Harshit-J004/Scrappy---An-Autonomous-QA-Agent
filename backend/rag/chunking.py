from typing import List, Dict
import re

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str, metadata: Dict) -> List[Dict]:
        """
        Splits text into chunks with overlap, preserving metadata.
        """
        chunks = []
        start = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size
            
            # If we are not at the end, try to find a natural break point (newline or space)
            if end < text_len:
                # Look for the last newline in the chunk
                last_newline = text.rfind('\n', start, end)
                if last_newline != -1 and last_newline > start + self.chunk_size // 2:
                    end = last_newline + 1
                else:
                    # Look for the last space
                    last_space = text.rfind(' ', start, end)
                    if last_space != -1 and last_space > start + self.chunk_size // 2:
                        end = last_space + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata.copy()
                })
            
            start = end - self.chunk_overlap
            # Ensure we always move forward
            if start >= end:
                start = end
        
        return chunks

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Processes a list of documents (dicts with 'text' and 'metadata') into chunks.
        """
        all_chunks = []
        for doc in documents:
            doc_chunks = self.split_text(doc['text'], doc['metadata'])
            all_chunks.extend(doc_chunks)
        return all_chunks
