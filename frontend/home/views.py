from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    token = request.session.get("access_token")

    if not token:
        return redirect("login")

    return render(request, "home/home.html")