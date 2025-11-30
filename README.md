# Autonomous QA Agent

An intelligent, autonomous QA agent capable of constructing a "testing brain" from project documentation and generating grounded test cases and Selenium scripts.

## Features
- **Knowledge Base Ingestion**: Parses PDF, Markdown, JSON, and HTML to build a RAG-based knowledge base.
- **Test Case Generation**: Uses Gemini 2.0 Flash to generate structured test cases grounded in your docs.
- **Selenium Script Generation**: Converts test cases into runnable Python Selenium scripts using real HTML selectors.
- **Modern UI**: Built with Streamlit for a clean, easy-to-use interface.

## 💎 UI Showcase

### Phase 01: Knowledge Base
![Knowledge Base](<img width="1024" height="471" alt="image" src="https://github.com/user-attachments/assets/27d4fc2a-0af1-445f-8f89-6d57db72d23a" />)


### Phase 02: Test Case Generation
![Test Cases](<img width="1024" height="445" alt="image" src="https://github.com/user-attachments/assets/26777750-a786-42d0-9c78-5293cf637b42" />)

### Phase 03: Script Generation
![Scripts](<img width="1024" height="479" alt="image" src="https://github.com/user-attachments/assets/f330b144-b0de-4811-88c5-dd213622e894" />_)


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
