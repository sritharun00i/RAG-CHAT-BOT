from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

# Create dummy PDF or text file
test_file_content = b"This is a test document about retrievel augmented generation."
test_file_name = "test_doc.txt"
with open(test_file_name, "wb") as f:
    f.write(test_file_content)

print(f"Created {test_file_name}")

# Ingest
print("Ingesting document...")
with open(test_file_name, "rb") as f:
    response = client.post("/ingest", files={"file": (test_file_name, f, "text/plain")})
    
if response.status_code == 200:
    print("Ingestion success:", response.json())
else:
    print("Ingestion failed:", response.text)
    exit(1)

# Query
print("Querying document...")
query_payload = {"query": "What is the document about?"}
response = client.post("/query", json=query_payload)

if response.status_code == 200:
    print("Query success:", response.json())
else:
    print("Query failed:", response.text)
    exit(1)

# Cleanup
os.remove(test_file_name)
print("Test completed.")
