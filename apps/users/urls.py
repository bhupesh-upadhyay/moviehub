from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-email/<str:uid>/<str:token>/", VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view()),
]