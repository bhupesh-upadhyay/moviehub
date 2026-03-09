from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, ProfileView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-email/<str:uid>/<str:token>/", VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view()),
    path("profile/", ProfileView.as_view(), name="profile"),
]