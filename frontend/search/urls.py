from django.urls import path
from .views import search

# frontend/search/urls.py
urlpatterns = [
    path("", search, name="search")
]