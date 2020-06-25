from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Message
from accounts.serializers import UserSerializer
from .serializers import MessageSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, HTMLFormRenderer, StaticHTMLRenderer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http.response import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from online_users.models import OnlineUserActivity
from datetime import timedelta


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return redirect('chat-api:chats')
    if not request.user.is_authenticated:
        return redirect('accounts-api:login')
    if request.method == 'GET':
        return render(request, 'index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chat-api:chats')


def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


def chat_view(request):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('accounts-api:login')
    if request.method == "GET":
        user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=1))
        active_users_queryset = user_activity_objects.exclude(user=request.user.id)
        """The id values of the online users"""
        active_users_id = []
        """ Online users """
        active_users = []
        for active_id in active_users_queryset:
            active_users_id.append(active_id.id)
        for active in active_users_queryset:
            active_users.append(active)
        normal_users_queryset_exclude_you_from_list = OnlineUserActivity.objects.exclude(user=request.user)
        """exclude online users from all users"""
        normal_users_queryset = normal_users_queryset_exclude_you_from_list.exclude(pk__in=active_users_id)
        normal_users = []
        for normal in normal_users_queryset:
            normal_users.append(normal)
        return render(request, 'chat.html',
                      {'users': normal_users,
                       'active_users': active_users})


def message_view(request, sender, receiver):
    """Render the template with required context variables"""
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        user_activity_objects = OnlineUserActivity.get_user_activities(timedelta(minutes=1))
        """excludes the current user from active user list"""
        active_users_queryset = user_activity_objects.exclude(user=request.user.id)
        """The id values of the online users"""
        active_users_id = []
        """ Online users """
        active_users = []
        for active_id in active_users_queryset:
            active_users_id.append(active_id.id)
        for active in active_users_queryset:
            active_users.append(active)
        normal_users_queryset_exclude_you_from_list = OnlineUserActivity.objects.exclude(user=request.user)
        """exclude online users from all users"""
        normal_users_queryset = normal_users_queryset_exclude_you_from_list.exclude(pk__in=active_users_id)
        normal_users = []
        for normal in normal_users_queryset:
            normal_users.append(normal)
        return render(request, 'messages.html',
                      {'users': normal_users,
                       'active_users': active_users,
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


class MessageCreateList(APIView):

    def get(self, request, sender=None, receiver=None):
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True)
        for message in messages:
            message.is_read = True
            message.save()
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


