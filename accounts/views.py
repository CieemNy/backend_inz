from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions, status

User = get_user_model()


# endpoint: display list of users

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'users-list'
