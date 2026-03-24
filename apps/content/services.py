from sentence_transformers import SentenceTransformer
import numpy as np

# will not download the model every time the django reload.
_model = None

# Lazy Loading
def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"   # 🔥 FORCE CPU
        )
    return _model

class EmbeddingService:

    @staticmethod
    def generate_embedding(text):
        model = get_model()
        return model.encode(text).tolist()
    
    @staticmethod
    def cosine_similarity(a, b):
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))