from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q

from .serializers import MovieSerializer
from .models import Movie
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
