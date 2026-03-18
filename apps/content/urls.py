from django.urls import path
from .views import MovieListView, MovieDetailView

# GET /api/content
urlpatterns = [
    path("movies/", MovieListView.as_view(), name='movielist'),
    path("movies/<int:pk>/", MovieDetailView.as_view(), name='moviedetail '),
]