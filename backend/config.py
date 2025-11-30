import os

class Config:
    # Storage paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DOCS_DIR = os.path.join(BASE_DIR, "backend", "storage", "raw_docs")
    CHECKOUT_DIR = os.path.join(BASE_DIR, "backend", "storage", "checkout")
    FAISS_INDEX_PATH = os.path.join(BASE_DIR, "backend", "storage", "faiss_index.bin")
    METADATA_PATH = os.path.join(BASE_DIR, "backend", "storage", "metadata.json")
    TEST_CASES_PATH = os.path.join(BASE_DIR, "backend", "storage", "test_cases.json")

    # Model settings
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Gemini API Key (User must provide this)
    # Gemini API Key (User must provide this)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

config = Config()
