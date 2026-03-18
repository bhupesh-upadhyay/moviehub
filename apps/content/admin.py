from django.contrib import admin
from .models import Movie, Actor, Genre

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year", "duration"]

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]