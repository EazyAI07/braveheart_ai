import os
import json
import numpy as np
import faiss
import openai
from app.core.config import PROCESSED_DIR, EMBEDDING_MODEL

# Load FAISS index
INDEX_PATH = PROCESSED_DIR / "bhat.index"
DOCSTORE_PATH = PROCESSED_DIR / "bhat_docs.json"

print("📦 Loading FAISS index and docstore...")
index = faiss.read_index(str(INDEX_PATH))

with open(DOCSTORE_PATH, "r", encoding="utf-8") as f:
    docstore = json.load(f)

def retrieve_context(query, top_k=5):
    """
    Retrieve top-k relevant chunks from the knowledge base for RAG
    """
    # Generate embedding for query
    resp = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    emb = np.array(resp.data[0].embedding).astype("float32")

    # Search FAISS
    D, I = index.search(np.array([emb]), top_k)

    # Fetch top-k documents
    results = [docstore[i]["content"] for i in I[0] if i < len(docstore)]
    context = "\n\n".join(results)

    return context
