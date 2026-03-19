from django.urls import path
from .views import MovieListAPIView, MovieDetailAPIView

# GET /api/content
urlpatterns = [
    path("movies/", MovieListAPIView.as_view(), name='movielist'),
    path("movies/<int:pk>/", MovieDetailAPIView.as_view(), name='moviedetail'),
]