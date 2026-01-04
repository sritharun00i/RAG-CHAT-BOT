from fastapi.testclient import TestClient
from app.main import app
import os

print("Importing app...")
client = TestClient(app)
print("App imported successfully.")

# Basic check
response = client.get("/docs")
assert response.status_code == 200
print("Docs endpoint accessible.")
