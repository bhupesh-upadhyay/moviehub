from django.core.management.base import BaseCommand
from apps.content.models import Movie, Genre, Actor
from apps.content.tmdb_service import TMDBService, map_movie_data, fetch_genres
import time
from apps.content.tasks import generate_movie_embedding

# python manage.py import_tmdb_movies --pages=5
class Command(BaseCommand):
    help = "Import movies from TMDB"

    def add_arguments(self, parser):
        parser.add_argument("--pages", type=int, default=1)

    def handle(self, *args, **kwargs):

        pages = kwargs["pages"]

        # Load genres
        genres_data = fetch_genres()
        genre_map = {}

        for g in genres_data["genres"]:
            genre_obj, _ = Genre.objects.get_or_create(name=g["name"])
            genre_map[g["id"]] = genre_obj

        for page in range(1, pages + 1):

            data = TMDBService.fetch_popular_movies(page)
            if not data:
                print("Failed to fetch data, skipping page")
                continue

            for item in data["results"]:

                movie_data = map_movie_data(item)
                
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=movie_data["tmdb_id"],
                    defaults=movie_data
                )

                # Genres
                genre_ids = item.get("genre_ids", [])
                movie.genres.set([
                    genre_map[gid] for gid in genre_ids if gid in genre_map
                ])

                # Actors
                credits = TMDBService.fetch_movie_credits(item["id"])
                if not credits:
                    continue
                actors = credits.get("cast", [])[:5]

                actor_objs = []
                for actor in actors:
                    actor_obj, _ = Actor.objects.get_or_create(name=actor["name"])
                    actor_objs.append(actor_obj)

                movie.actors.set(actor_objs)
                # 🔥 prevent rate limit
                time.sleep(0.5)

        self.stdout.write(self.style.SUCCESS("Movies imported successfully"))
        
        self.stdout.write("Starting embedding tasks...")
        for movie in Movie.objects.filter(embedding__isnull=True)[:50]:
            generate_movie_embedding.delay(movie.id)

        self.stdout.write(self.style.SUCCESS("Embedding tasks queued"))
        
    