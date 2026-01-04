# Domain-Aware RAG Chatbot

## Setup

1. **Install Dependencies**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Environment Variables**:
    Create a `.env` file from the example:
    ```bash
    cp .env.example .env
    ```
    Add your `OPENAI_API_KEY` to the `.env` file.

## Usage

1. **Start the API Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

2. **Ingest Documents**:
    Use the `/ingest` endpoint to upload a PDF or Text file.
    - URL: `http://localhost:8000/docs` (Swagger UI)
    - POST `/ingest`

3. **Query**:
    Use the `/query` endpoint to ask questions.
    - POST `/query`
    - Body: `{"query": "What is the summary of the document?"}`

## Project Structure
- `app/ingestion.py`: Handles document loading and splitting.
- `app/vector_store.py`: Manages ChromaDB.
- `app/rag.py`: RAG chain logic.
- `app/main.py`: FastAPI application.
