from django.shortcuts import render, redirect
from apps.users.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
import requests

API_BASE = "http://localhost:8000/api/users"

# Create your views here.
def register(request):
    if request.method == 'POST':
        payload = {
            "email": request.POST.get('email'),
            'username': request.POST.get('username'),
            'password': request.POST.get('password'),
        }
        response = requests.post(f"{API_BASE}/register/", json=payload)
    
        if response.status_code == 201:
            messages.success(request, "Account created successfully")
            return redirect("login")
        else:
            messages.error(request, response.json())
    
    return render(request, "auth/register.html")


import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        payload = {
            "email": request.POST.get("email"),
            "password": request.POST.get("password"),
        }

        response = requests.post(
            f"{API_BASE}/login/",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            
            # store token in session
            request.session["access_token"] = data.get("access")
            
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "auth/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


"""
User submits form
     ↓
Django frontend view
     ↓
Calls /api/users/*
     ↓
API returns token
     ↓
Stored in session
     ↓
Used for future API calls

"""


