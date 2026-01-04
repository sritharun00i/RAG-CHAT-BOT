try:
    import chromadb
    print("ChromaDB imported successfully")
    print(f"Version: {chromadb.__version__}")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")

import sqlite3
print(f"SQLite version: {sqlite3.sqlite_version}")
