from django.db import models
from apps.users.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    release_year = models.IntegerField()
    duration = models.IntegerField(
        help_text="Duration in seconds"
    )
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(
        Actor,
        related_name="movies"
    )
    thumbnail = models.ImageField(upload_to="thumbnails/")
    video_url = models.URLField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    embedding = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watchlist_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "movie")
        
    def __str__(self):
        return f"{self.user.email} -> {self.movie.title}"
    
"""
At scale, systems use:   
Redis → store live progress
DB → store final state
"""
class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='watch_history')

    progress_seconds = models.IntegerField()
    completed = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.email} → {self.movie.title}"