from django.urls import path
from .views import ContentDetailView, ContentListView

# GET /api/content
urlpatterns = [
    path("", ContentListView.as_view()),
    path("<int:pk>/", ContentDetailView.as_view()),
]