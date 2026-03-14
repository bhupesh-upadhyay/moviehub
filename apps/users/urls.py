from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, ProfileView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-email/<str:uid>/<str:token>/", VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view()),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("forgot-password/", ForgotPasswordView.as_view(), name='forget-password'),
    path("reset-password/<uid>/<token>/", ResetPasswordView.as_view(), name='reset-password')
]