from django.shortcuts import render

# Create your views here.
# frontend/search/views.py

import requests

def search(request):
    query = request.GET.get("q", "")
    token = request.session.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"http://localhost:8000/api/movies/semantic-search/?q={query}",
        headers=headers
    )

    movies = response.json() if response.status_code == 200 else []

    return render(request, "search/partials/results.html", {"movies": movies})