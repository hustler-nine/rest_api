from . import views
from django.urls import path, re_path, include


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', include('rest_auth.urls')),
    path('register/', views.UserCreate.as_view(), name='register'),
]
