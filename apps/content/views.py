from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import MovieSerializer
from .models import Movie
# Create your views here.

class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["genres", "actors"]
    search_fields = ["title", "description"]
    
class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
