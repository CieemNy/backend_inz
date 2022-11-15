from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'name',
            'surname',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'is_leader',
            'is_member',
            'is_company'
        ]
