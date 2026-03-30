from celery import shared_task
from .models import Movie
from .services import EmbeddingService
import csv
from io import StringIO


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def generate_movie_embedding(self, movie_id):
    # from .services import EmbeddingService
    # from .models import Movie
    movie = Movie.objects.get(id=movie_id)
    text = f"{movie.title} {movie.description}"
    embedding = EmbeddingService.generate_embedding(text)
    movie.embedding = embedding
    movie.save()
    
    
@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def import_movies_from_csv(self, file_data):

    csv_file = StringIO(file_data)
    reader = csv.DictReader(csv_file)

    for row in reader:
        Movie.objects.create(
            title=row["title"],
            description=row["description"],
            release_year=int(row["release_year"]),
            duration=int(row["duration"]),
        )

    return "Import completed"
# trigger
# transaction.on_commit(
#     lambda: generate_movie_embedding.delay(movie.id)
# )