from rest_framework import serializers
from .models import Movie, Genre, Actor

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
    # genres = serializers.StringRelatedField(many=True)
    # actors = serializers.StringRelatedField(many=True)
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = "__all__"