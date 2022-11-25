from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import *


User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    company = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    team = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
            'is_company',
            'is_verified'
        ]


class CompanySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Company
        fields = [
            'id',
            'user',
            'name',
            'description',
            'contact_number',
            'contact_email',
            'main_front',
            'main_back',
            'occupied_places',
            'places'
        ]


class TeamSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Team
        fields = [
            'id',
            'user',
            'name',
            'occupied_places',
            'places',
            'creation_date',
        ]

    def validate(self, data):
        occupied_places = self.context.get('occupied_places')
        if occupied_places == data['places']:
            raise serializers.ValidationError("Osiągnięto limit osób w drużynie")
        return data


class MembersSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    team = serializers.ReadOnlyField(source='team.name')

    class Meta:
        model = Members
        fields = [
            'id',
            'user',
            'team',
        ]
