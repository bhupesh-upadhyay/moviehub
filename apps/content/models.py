from django.db import models

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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title