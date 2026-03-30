from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from rest_framework import status
from .serializers import MovieSerializer, WatchlistSerializer, WatchHistorySerializer, WatchHistory, MovieListSerializer
from .models import Movie, Watchlist, WatchHistory
from .services import EmbeddingService
from .utils import cosine_similarity
# Create your views here.

class MovieListAPIView(APIView):
    def get(self, request):
        queryset = Movie.objects.all()
        # 🔍 SEARCH
        search = request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        # 🎯 FILTER BY GENRE
        genre_id = request.query_params.get("genres")
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        # 🎯 FILTER BY ACTOR
        actor_id = request.query_params.get("actors")
        if actor_id:
            queryset = queryset.filter(actors__id=actor_id)

        # 📄 PAGINATION
        page = request.query_params.get("page", 1)
        page_size = 10

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        serializer = MovieSerializer(page_obj, many=True)

        return Response({
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": int(page),
            "results": serializer.data
        })
  
class MovieDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)

        serializer = MovieSerializer(movie)

        return Response(serializer.data)


# POST   /watchlist/        → add movie
# GET    /watchlist/        → list user movies
# DELETE /watchlist/{id}/   → remove movie
# TODO We can convert it to Generic too 👇
"""
class WatchlistListView(ListAPIView)
class WatchlistCreateView(CreateAPIView)
class WatchlistDeleteView(DestroyAPIView)
"""


class WatchlistCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = WatchlistSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    

class WatchlistListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        watchlist = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)
    

class WatchlistDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            watchlist = Watchlist.objects.get(
                id=pk,
                user=request.user
            )
        except Watchlist.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=404
            )
        watchlist.delete()
        return Response({"message": "Removed"}, status=200)
    
# POST /api/progress/        → update progress
# GET  /api/continue/        → list unfinished movies

class WatchProgressAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = WatchHistorySerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)

        return Response(serializer.errors, status=400)
    
class ContinueWatchingAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = WatchHistory.objects.filter(
            user=request.user,
            completed=False
        ).order_by("-updated_at")

        serializer = WatchHistorySerializer(queryset, many=True)

        return Response(serializer.data)
    
# GET /api/movies/trending/
"""
Get recent activity
Get total activity
Compute weighted score
Sort movies
Return ranked list

Ranking system
Aggregation queries
Time-based analytics
OTT recommendation logic

permormance:
    loops through all movies
TODO:
    annotations
    materialized views
    caching (Redis)
At scale:
    Trending is NOT calculated per request
Instead:
    Celery job runs every 5 min
    ↓
    computes trending
    ↓
    stores in Redis
    ↓
    API reads from Redis
"""
class TrendingMoviesAPIView(APIView):

    def get(self, request):

        recent_threshold = now() - timedelta(days=7)

        # recent views
        recent_views = WatchHistory.objects.filter(
            updated_at__gte=recent_threshold
        ).values("movie").annotate(
            recent_count=Count("id")
        )

        # total views
        total_views = WatchHistory.objects.values("movie").annotate(
            total_count=Count("id")
        )

        # dict mapping
        recent_dict = {
            item["movie"]: item["recent_count"]
            for item in recent_views
        }

        total_dict = {
            item["movie"]: item["total_count"]
            for item in total_views
        }

        # compute scores
        movie_scores = []

        for movie in Movie.objects.all():

            recent = recent_dict.get(movie.id, 0)
            total = total_dict.get(movie.id, 0)

            score = (recent * 2) + total

            movie_scores.append((movie, score))

        # sort
        movie_scores.sort(key=lambda x: x[1], reverse=True)

        # extract movies
        movies = [item[0] for item in movie_scores]

        # 🔥 LIMIT (top N)
        limit = request.query_params.get("limit", 10)

        try:
            limit = int(limit)
        except ValueError:
            limit = 10

        movies = movies[:limit]

        # 🔥 OPTIONAL PAGINATION
        page = request.query_params.get("page")

        if page:
            paginator = Paginator(movies, limit)
            page_obj = paginator.get_page(page)

            serializer = MovieSerializer(page_obj, many=True)

            return Response({
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "results": serializer.data
            })

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

class SemanticSearchAPIView(APIView):

    def get(self, request):

        query = request.query_params.get("q")

        if not query:
            return Response({"error": "Query required"}, status=400)

        query_embedding = EmbeddingService.generate_embedding(query)

        results = []

        # for movie in Movie.objects.exclude(embedding=None):
        for movie in Movie.objects.filter(embedding__isnull=False):

            score = cosine_similarity(query_embedding, movie.embedding)

            results.append((movie, score))
        results.sort(key=lambda x: x[1], reverse=True)

        top_movies = [item[0] for item in results[:10]]

        serializer = MovieListSerializer(top_movies, many=True)

        return Response(serializer.data)
    
    
# TODO: alter the api for million records
"""
class SemanticSearchAPIView(APIView):

    def get(self, request):

        query = request.query_params.get("q")

        if not query:
            return Response({"error": "Query required"}, status=400)

        # 🔍 Step 1: Reduce dataset
        queryset = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )[:100]

        query_embedding = EmbeddingService.generate_embedding(query)

        results = []

        for movie in queryset:

            if not movie.embedding:
                continue

            score = cosine_similarity(query_embedding, movie.embedding)

            results.append((movie, score))

        results.sort(key=lambda x: x[1], reverse=True)

        movies = [item[0] for item in results[:10]]

        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)
"""

class SimilarViewsAPIView(APIView):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error':'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not movie.embedding:
            return Response({'error':'No embeddings available'}, status=status.HTTP_400_BAD_REQUEST)
        
        movie_genres = set(movie.genres.values_list("id", flat=True))
        result = []
        
        for m in Movie.objects.exclude(id=movie.id).exclude(embedding__isnull=True):
            # Embedding similarity
            sim_score = cosine_similarity(movie.embedding, m.embedding)
            
            # Genre boost
            m_genres = set(m.genres.values_list("id", flat=True))
            common_genres = movie_genres.intersection(m_genres)
            
            genre_score = len(common_genres) * 0.1  # weight
            
            # 3. Final score
            final_score = sim_score + genre_score
            
            result.append((m, final_score))
        
        result.sort(key=lambda x: x[1], reverse=True)
        top_movies = [item[0] for item in result[:10]]
        serializers = MovieListSerializer(top_movies, many=True)
        return Response(serializers.data)
        
        