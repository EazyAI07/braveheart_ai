import faiss
import numpy as np

class VectorStore:
    def __init__(self, index_path: str):
        self.index = faiss.read_index(index_path)

    def search(self, embedding, top_k=4):
        D, I = self.index.search(
            np.array([embedding]).astype("float32"),
            top_k
        )
        return I[0]
