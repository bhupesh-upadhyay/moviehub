from filelock import FileLock
from django.conf import settings
from fastembed import TextEmbedding

_model = None
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _load_lock_path():
    return settings.FASTEMBED_CACHE_DIR / ".embedding_model.lock"


def get_model():
    """Load TextEmbedding once per process; file lock prevents parallel broken downloads."""
    global _model
    if _model is not None:
        return _model

    settings.FASTEMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    lock = FileLock(str(_load_lock_path()), timeout=900)
    with lock:
        if _model is None:
            _model = TextEmbedding(
                model_name=EMBEDDING_MODEL_NAME,
                cache_dir=str(settings.FASTEMBED_CACHE_DIR),
            )
    return _model


def warm_embedding_model():
    """Call from Celery worker_process_init so the ONNX file finishes before tasks run."""
    get_model()


class EmbeddingService:

    @staticmethod
    def generate_embedding(text):
        model = get_model()
        vector = next(model.embed([text]))
        return vector.tolist()
