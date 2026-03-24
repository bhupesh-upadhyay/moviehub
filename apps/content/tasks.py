from celery import shared_task
from .models import Movie
from .services import EmbeddingService


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def generate_movie_embedding(self, movie_id):
    # from .services import EmbeddingService
    # from .models import Movie
    movie = Movie.objects.get(id=movie_id)
    text = f"{movie.title} {movie.description}"
    embedding = EmbeddingService.generate_embedding(text)
    movie.embedding = embedding
    movie.save()
    
    
# trigger
# transaction.on_commit(
#     lambda: generate_movie_embedding.delay(movie.id)
# )