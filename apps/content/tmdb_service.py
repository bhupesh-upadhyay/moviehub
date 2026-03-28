import requests
from django.conf import settings
from apps.content.models import Genre
import time

class TMDBService:

    BASE_URL = "https://api.themoviedb.org/3"
    
    @staticmethod
    def safe_request(url, params, retries=5):

        for attempt in range(retries):
            try:
                response = requests.get(url, params=params, timeout=3)
                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:   
                wait = 2 ** attempt  # exponential backoff
                print(f"Retry {attempt+1} failed: {e}, retrying in {wait}s")
                time.sleep(wait)
        return None

    @staticmethod
    def fetch_popular_movies(page=1):
        url = f"{TMDBService.BASE_URL}/movie/popular"

        params = {
            "api_key": settings.TMDB_API_KEY,
            "page": page,
        }
        return TMDBService.safe_request(url, params)

    @staticmethod
    def fetch_movie_credits(movie_id):
        url = f"{TMDBService.BASE_URL}/movie/{movie_id}/credits"

        params = {
            "api_key": settings.TMDB_API_KEY,
        }
        return TMDBService.safe_request(url, params)

def map_movie_data(data):
    return {
        "tmdb_id": data["id"],  # 🔥 IMPORTANT
        "title": data["title"],
        "description": data.get("overview", ""),
        "release_year": int(data["release_date"][:4]) if data.get("release_date") else 2020,
        "duration": 7200,
        "thumbnail": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}",
    }
    
def fetch_genres():
    url = f"{TMDBService.BASE_URL}/genre/movie/list"

    params = {
        "api_key": settings.TMDB_API_KEY,
    }

    return TMDBService.safe_request(url, params)