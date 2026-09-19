from django.urls import path
from .views import (
    WatchlistCreateView,
    WatchlistListView,
    WatchlistDeleteView,
    WatchProgressAPIView,
    ContinueWatchingAPIView,
    GenreListAPIView,
    MovieListAPIView,
    MovieDetailAPIView,
    SemanticSearchAPIView,
    SimilarViewsAPIView,
)

# GET /api/content
urlpatterns = [
    path("genres/", GenreListAPIView.as_view(), name="genrelist"),
    path("movies/", MovieListAPIView.as_view(), name='movielist'),
    path("movies/<int:pk>/", MovieDetailAPIView.as_view(), name='moviedetail'),
    path("watchlist/", WatchlistCreateView.as_view()),
    path("watchlist/list/", WatchlistListView.as_view()),
    path("watchlist/<int:pk>/", WatchlistDeleteView.as_view()),
    path("progress/", WatchProgressAPIView.as_view()),
    path("continue/", ContinueWatchingAPIView.as_view()),
    path("movies/semantic-search/", SemanticSearchAPIView.as_view()),
    path("movies/<int:movie_id>/similar/", SimilarViewsAPIView.as_view())
]