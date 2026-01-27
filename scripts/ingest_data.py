import os
import json
import csv
from pathlib import Path
import numpy as np
import faiss
import openai
from docx import Document
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()
# --------------------------------------------------
# CONFIG
# --------------------------------------------------
RAW_DIR = Path("app/data/raw")
PROCESSED_DIR = Path("app/data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = PROCESSED_DIR / "bhat.index"
DOCSTORE_PATH = PROCESSED_DIR / "bhat_docs.json"

EMBEDDING_MODEL = "text-embedding-3-large"

openai.api_key = os.getenv("OPENAI_API_KEY")

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def load_docx(path):
    """Extract clean paragraphs from DOCX"""
    doc = Document(path)
    chunks = []
    for p in doc.paragraphs:
        text = p.text.strip()
        if len(text) > 40:
            chunks.append(text)
    return chunks


def load_csv(path):
    """Convert CSV rows into text chunks"""
    chunks = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            text = (
                f"{row['Substance']} na called {row['Pidgin Name']} for Nigerian Pidgin. "
                f"English meaning: {row['English Meaning']}. "
                f"Notes: {row['Notes']}."
            )
            chunks.append({
                "content": text,
                "metadata": {
                    "category": "substance_names",
                    "substance_type": row["Substance"].lower(),
                    "language": "bilingual",
                    "region": ["nigeria"],
                    "source": path.name
                }
            })
    return chunks


def load_jsonl(path):
    """Load already structured JSONL RAG docs"""
    docs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))
    return docs


def embed_text(text):
    """Create OpenAI embedding"""
    resp = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return resp.data[0].embedding


# --------------------------------------------------
# INGEST PIPELINE
# --------------------------------------------------
documents = []

print("🔍 Loading datasets...")

# DOCX files
for docx_file in RAW_DIR.glob("*.docx"):
    paragraphs = load_docx(docx_file)
    for p in paragraphs:
        documents.append({
            "content": p,
            "metadata": {
                "category": "clinical_faq",
                "language": "english",
                "region": ["sub_saharan_africa"],
                "source": docx_file.name
            }
        })

# CSV files
for csv_file in RAW_DIR.glob("*.csv"):
    documents.extend(load_csv(csv_file))

# JSONL files
for jsonl_file in RAW_DIR.glob("*.jsonl"):
    documents.extend(load_jsonl(jsonl_file))

print(f"✅ Loaded {len(documents)} knowledge chunks")

# --------------------------------------------------
# EMBEDDINGS + FAISS
# --------------------------------------------------
print("🧠 Generating embeddings...")
embeddings = []

for doc in tqdm(documents):
    emb = embed_text(doc["content"])
    embeddings.append(emb)

embeddings = np.array(embeddings).astype("float32")

print("📦 Building FAISS index...")
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, str(INDEX_PATH))

# Save document store
with open(DOCSTORE_PATH, "w", encoding="utf-8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=2)

print("🎉 Ingestion complete!")
print(f"FAISS index saved to: {INDEX_PATH}")
print(f"Document store saved to: {DOCSTORE_PATH}")
