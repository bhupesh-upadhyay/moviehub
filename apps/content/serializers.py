from rest_framework import serializers
from .models import Movie, Genre, Actor, Watchlist, WatchHistory

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]
# genres = GenreSerializer(many=True)

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "name"]

class MovieSerializer(serializers.ModelSerializer):
    
    """
    If we already have fields = "__all__", why did we explicitly define:
        to avoid this response: (not human readable get ids)
        {
        "genres": [1, 2],
        "actors": [3, 5]
        }
        For each related object
            ↓
            call __str__()
            ↓
            return string
            str(Genre(name="Sci-Fi")) → "Sci-Fi"
    """
    genres = serializers.StringRelatedField(many=True)
    actors = serializers.StringRelatedField(many=True)
    # genres = GenreSerializer(many=True)
    # actors = ActorSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "release_year",
            "duration",
            "genres",
            "actors",
            "thumbnail",
            "video_url",
            "created_at",
        ]
        
class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Watchlist
        fields = ["id", "movie", "movie_id", "created_at"]
        
    def create(self, validated_data):
        user = self.context["request"].user
        movie_id = validated_data["movie_id"]

        movie = Movie.objects.get(id=movie_id)

        watchlist, created = Watchlist.objects.get_or_create(
            user=user,
            movie=movie
        )

        return watchlist
    

class WatchHistorySerializer(serializers.ModelSerializer):

    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WatchHistory
        fields = ["id", "movie", "movie_id", "progress_seconds", "completed"]

    def create(self, validated_data):
        user = self.context["request"].user
        movie_id = validated_data["movie_id"]

        movie = Movie.objects.get(id=movie_id)

        obj, created = WatchHistory.objects.update_or_create(
            user=user,
            movie=movie,
            defaults={
                "progress_seconds": validated_data["progress_seconds"],
                "completed": validated_data.get("completed", False),
            }
        )
        return obj
    
  
# Light weight Movie search only    
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ["id", "title", "thumbnail"]