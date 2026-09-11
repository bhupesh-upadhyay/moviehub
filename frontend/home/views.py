from django.shortcuts import render, redirect
import requests


# Create your views here.
API_BASE = "http://localhost:8000/api"


def home(request):
    token = request.session.get("access_token")

    # if not token:
    #     return redirect("login")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(f"{API_BASE}/movies")
    
        if response.status_code == 200:
            movies = response.json()
        else:
            movies = []
    except Exception:
        movies = []
        
    return render(request, "home/home.html", context={"movies":movies})


def movie_detail(request, id):
    token = request.session.get("access_token")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"http://localhost:8000/api/movies/{id}/",
        headers=headers
    )

    movie = response.json() if response.status_code == 200 else None

    return render(request, "home/detail.html", {"movie": movie})