import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

def load_documents(source_path: str) -> List[Document]:
    """
    Load documents from a file path. Supports PDF and txt.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"File not found: {source_path}")

    if source_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(source_path)
        return loader.load()
    elif source_path.lower().endswith(".txt"):
        loader = TextLoader(source_path)
        return loader.load()
    else:
        raise ValueError(f"Unsupported file type: {source_path}")

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def get_embeddings():
    """
    Get the embedding model.
    """
    # Ensure OPENAI_API_KEY is key in environment
    if not os.getenv("OPENAI_API_KEY"):
         print("Warning: OPENAI_API_KEY not found in environment variables.")
    return OpenAIEmbeddings()
