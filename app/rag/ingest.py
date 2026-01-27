import os
import faiss
import openai
from pathlib import Path
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

def embed_text(text: str):
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def ingest_documents(data_dir="app/data/raw"):
    texts = []
    metadatas = []

    for file in Path(data_dir).glob("*.md"):
        content = file.read_text(encoding="utf-8")
        texts.append(content)
        metadatas.append({"source": file.name})

    embeddings = []
    for text in tqdm(texts):
        embeddings.append(embed_text(text))

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    faiss.write_index(index, "app/data/processed/bhat.index")

    return texts, metadatas
