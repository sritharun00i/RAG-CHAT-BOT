import os
import shutil
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from app.ingestion import get_embeddings

PERSIST_DIRECTORY = "./faiss_db"

def setup_vector_store(documents: List[Document], reset: bool = False):
    """
    Initialize and persist the FAISS vector store with documents.
    """
    if reset and os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)

    embedding_function = get_embeddings()
    
    # Create FAISS index
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embedding_function
    )
    
    # Persist to disk
    vectorstore.save_local(PERSIST_DIRECTORY)
    
    return vectorstore

def get_retriever(search_kwargs: dict = {"k": 3}) -> VectorStoreRetriever:
    """
    Get the retriever from the persisted vector store.
    """
    embedding_function = get_embeddings()
    
    if not os.path.exists(PERSIST_DIRECTORY):
        raise ValueError("Vector store not found. Please ingest documents first.")
        
    # Load from disk
    vectorstore = FAISS.load_local(
        PERSIST_DIRECTORY, 
        embedding_function,
        allow_dangerous_deserialization=True
    )
    
    return vectorstore.as_retriever(search_kwargs=search_kwargs)
