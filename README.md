# Autonomous QA Agent

An intelligent, autonomous QA agent capable of constructing a "testing brain" from project documentation and generating grounded test cases and Selenium scripts.

## Features
- **Knowledge Base Ingestion**: Parses PDF, Markdown, JSON, and HTML to build a RAG-based knowledge base.
- **Test Case Generation**: Uses Gemini 2.0 Flash to generate structured test cases grounded in your docs.
- **Selenium Script Generation**: Converts test cases into runnable Python Selenium scripts using real HTML selectors.
- **Modern UI**: Built with Streamlit for a clean, easy-to-use interface.

## 💎 UI Showcase

### Phase 01: Knowledge Base
![Knowledge Base](docs/images/knowledge_base.png)

### Phase 02: Test Case Generation
![Test Cases](docs/images/test_cases.png)

### Phase 03: Script Generation
![Scripts](docs/images/scripts.png)

## Setup

1. **Prerequisites**:
   - Python 3.9+
   - A Google Gemini API Key

2. **Installation**:
   ```bash
   pip install -r qa-agent/requirements.txt
   ```

3. **Environment**:
   Set your Google API Key:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your_api_key_here"
   ```

## Usage

1. **Start the Backend**:
   ```bash
   cd qa-agent
   uvicorn backend.main:app --reload
   ```

2. **Start the Frontend**:
   ```bash
   streamlit run ui/app.py
   ```

3. **Workflow**:
   - Go to **1. Knowledge Base**: Upload `docs/product_specs.md`, `docs/ui_ux_guide.txt`, etc., and `docs/checkout.html`. Click "Build Knowledge Base".
   - Go to **2. Test Cases**: Enter a query (e.g., "Verify discount codes"). Generate and select a test case.
   - Go to **3. Selenium Scripts**: Generate the script for the selected test case and download it.

## Architecture
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **RAG**: SentenceTransformers (`all-MiniLM-L6-v2`) + FAISS
- **LLM**: Gemini 2.0 Flash (via `google-generativeai`)

## Project Structure
```
qa-agent/
  backend/          # FastAPI app & logic
    rag/            # RAG pipeline (parsers, chunking, vector store)
    agents/         # Gemini agents
  ui/               # Streamlit app
  docs/             # Example assets
```
