from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.


class UserCreate(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

