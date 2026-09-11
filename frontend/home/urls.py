from django.urls import path
from .views import home, movie_detail

urlpatterns = [
    path("", home, name="home"),
    path("movies/<int:id>/", movie_detail, name="movie_detail")
]