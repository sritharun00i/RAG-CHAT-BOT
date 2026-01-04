import os
from dotenv import load_dotenv
from app.ingestion import load_documents, split_documents
from app.vector_store import setup_vector_store

# Load env to get API key
load_dotenv()
print(f"API Key present: {'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'].startswith('sk-')}")

# Create dummy PDF
from reportlab.pdfgen import canvas
pdf_file = "test_debug.pdf"
c = canvas.Canvas(pdf_file)
c.drawString(100, 750, "Hello World. This is a test PDF for RAG.")
c.save()

try:
    print("Loading documents...")
    docs = load_documents(pdf_file)
    print(f"Loaded {len(docs)} docs.")
    
    print("Splitting documents...")
    chunks = split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")
    
    print("Setting up vector store...")
    setup_vector_store(chunks)
    print("Vector store setup complete.")

except Exception as e:
    import traceback
    traceback.print_exc()

finally:
    if os.path.exists(pdf_file):
        os.remove(pdf_file)
