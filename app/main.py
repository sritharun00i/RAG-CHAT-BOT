import os
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.ingestion import load_documents, split_documents
from app.vector_store import setup_vector_store, get_retriever
from app.rag import build_chain

# Load environment variables
load_dotenv()

app = FastAPI(title="Domain-Aware RAG Chatbot")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.on_event("startup")
async def startup_event():
    # Optional: check for OPENAI_API_KEY
    if not os.getenv("OPENAI_API_KEY"):
        print("WARNING: OPENAI_API_KEY is not set.")

@app.post("/ingest")
async def ingest_documents(file: UploadFile = File(...)):
    """
    Ingest a document (PDF or Text) into the vector store.
    """
    try:
        # Save temp file
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process document
        docs = load_documents(file_path)
        chunks = split_documents(docs)
        setup_vector_store(chunks)
        
        # Cleanup
        os.remove(file_path)
        
        return {"message": "Document ingested successfully", "chunks": len(chunks)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Query the RAG system.
    """
    try:
        retriever = get_retriever()
        chain = build_chain(retriever)
        
        response = chain.invoke({"input": request.query})
        
        answer = response["answer"]
        # Extract source metadata if available
        sources = [doc.metadata.get("source", "unknown") for doc in response.get("context", [])]
        # Deduplicate sources
        sources = list(set(sources))
        
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
