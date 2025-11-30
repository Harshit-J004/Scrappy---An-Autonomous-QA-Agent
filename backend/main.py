from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from typing import List
from backend.config import config

from backend.rag.parsers import DocumentParser
from backend.rag.chunking import TextChunker
from backend.rag.embeddings import EmbeddingGenerator
from backend.rag.vector_store import VectorStore
from backend.agents.test_case_agent import TestCaseAgent
from backend.agents.script_agent import ScriptAgent
from pydantic import BaseModel

app = FastAPI(title="Autonomous QA Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "QA Agent Backend is running"}

@app.post("/upload_docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    if not os.path.exists(config.RAW_DOCS_DIR):
        os.makedirs(config.RAW_DOCS_DIR)
    
    saved_files = []
    for file in files:
        file_path = os.path.join(config.RAW_DOCS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    
    return {"message": f"Uploaded {len(saved_files)} files", "files": saved_files}

@app.post("/upload_checkout")
async def upload_checkout(file: UploadFile = File(...)):
    if not os.path.exists(config.CHECKOUT_DIR):
        os.makedirs(config.CHECKOUT_DIR)
        
    file_path = os.path.join(config.CHECKOUT_DIR, "checkout.html")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": "Checkout HTML uploaded successfully"}



# Global instances (lazy loading recommended in prod, but fine here)
chunker = TextChunker()
# EmbeddingGenerator and VectorStore will be initialized on first use or startup
# to avoid long load times if not needed immediately, but for simplicity:
embedding_gen = None 
vector_store = VectorStore()
test_agent = None
script_agent = None

def get_components():
    global embedding_gen, test_agent, script_agent
    if embedding_gen is None:
        embedding_gen = EmbeddingGenerator()
    if test_agent is None:
        try:
            test_agent = TestCaseAgent()
        except Exception as e:
            print(f"Warning: Could not init TestCaseAgent (check API Key): {e}")
    if script_agent is None:
        try:
            script_agent = ScriptAgent()
        except Exception as e:
            print(f"Warning: Could not init ScriptAgent (check API Key): {e}")
    return embedding_gen, test_agent, script_agent

@app.post("/build_kb")
async def build_kb():
    # 1. Load Documents
    raw_docs = []
    if os.path.exists(config.RAW_DOCS_DIR):
        for filename in os.listdir(config.RAW_DOCS_DIR):
            path = os.path.join(config.RAW_DOCS_DIR, filename)
            text = ""
            if filename.endswith(".pdf"):
                text = DocumentParser.parse_pdf(path)
            elif filename.endswith(".json"):
                text = DocumentParser.parse_json(path)
            else:
                text = DocumentParser.parse_text(path)
            
            raw_docs.append({"text": text, "metadata": {"source": filename}})

    # 2. Load Checkout HTML (as text for RAG)
    checkout_path = os.path.join(config.CHECKOUT_DIR, "checkout.html")
    if os.path.exists(checkout_path):
        html_content = DocumentParser.parse_text(checkout_path)
        html_text = DocumentParser.parse_html_text(html_content)
        raw_docs.append({"text": html_text, "metadata": {"source": "checkout.html", "type": "html_content"}})

    if not raw_docs:
        return {"message": "No documents found to build KB."}

    # 3. Chunking
    chunks = chunker.chunk_documents(raw_docs)

    # 4. Embeddings & Vector Store
    emb_gen, _, _ = get_components()
    texts = [c["text"] for c in chunks]
    embeddings = emb_gen.generate_embeddings(texts)
    
    vector_store.create_index(embeddings, [c["metadata"] for c in chunks]) # Storing metadata only, text is in chunks but we need to retrieve text too.
    # Wait, vector_store.create_index stores metadata. We should probably store the text in metadata or a separate store.
    # For simplicity, let's add text to metadata.
    full_metadata = []
    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"].copy()
        meta["text"] = chunk["text"]
        full_metadata.append(meta)
    
    vector_store.create_index(embeddings, full_metadata)

    return {"message": f"Knowledge Base Built. Processed {len(raw_docs)} docs into {len(chunks)} chunks."}

class TestCaseRequest(BaseModel):
    query: str

@app.post("/generate_test_cases")
async def generate_test_cases(request: TestCaseRequest):
    emb_gen, t_agent, _ = get_components()
    print("Test Agent: ", t_agent)
    if not t_agent:
        raise HTTPException(status_code=500, detail=f"Test Agent not initialized (check API Key). Agent: {t_agent}")
    
    # RAG Retrieval
    query_emb = emb_gen.generate_query_embedding(request.query)
    context_chunks = vector_store.search(query_emb, k=5)
    
    # Generation
    result = t_agent.generate_test_cases(request.query, context_chunks)
    
    # Save to file
    import json
    with open(config.TEST_CASES_PATH, 'w') as f:
        json.dump(result, f, indent=2)
        
    return result

class ScriptRequest(BaseModel):
    test_case: dict

@app.post("/generate_script")
async def generate_script(request: ScriptRequest):
    emb_gen, _, s_agent = get_components()
    if not s_agent:
        raise HTTPException(status_code=500, detail="Script Agent not initialized (check API Key).")

    # Load HTML
    checkout_path = os.path.join(config.CHECKOUT_DIR, "checkout.html")
    if not os.path.exists(checkout_path):
        raise HTTPException(status_code=404, detail="checkout.html not found.")
    
    html_content = DocumentParser.parse_text(checkout_path)
    elements_schema = DocumentParser.parse_html_structure(html_content)
    
    # RAG Retrieval (Context for script)
    # We use the test case description/steps as query
    query = f"{request.test_case.get('feature', '')} {request.test_case.get('scenario_type', '')} {' '.join(request.test_case.get('steps', []))}"
    query_emb = emb_gen.generate_query_embedding(query)
    context_chunks = vector_store.search(query_emb, k=3)

    script = s_agent.generate_script(request.test_case, html_content, elements_schema, context_chunks)
    
    return {"script": script}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
