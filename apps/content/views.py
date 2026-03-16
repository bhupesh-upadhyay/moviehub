from django.shortcuts import render
from .models import Content
from .serializers import ContentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
# Create your views here.

class ContentListView(ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    
    
class ContentDetailView(RetrieveAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer