from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('messages/<int:sender>/<int:receiver>/', views.MessageCreateList.as_view(), name='message-detail'),
    path('messages/', views.MessageCreateList.as_view(), name='message-list'),
    path('chat/', views.user_list, name='users')

]