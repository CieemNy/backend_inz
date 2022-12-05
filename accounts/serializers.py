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
    user = serializers.ReadOnlyField(source='user.id')
    companyMan = serializers.SerializerMethodField()

    def get_companyMan(self, obj):
        return f'{obj.user.name} {obj.user.surname}'

    class Meta:
        model = Company
        fields = [
            'id',
            'user',
            'name',
            'description',
            'contact_number',
            'contact_email',
            'occupied_places',
            'places',
            'companyMan'
        ]


class TeamSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')
    leader = serializers.SerializerMethodField()

    def get_leader(self, obj):
        return f'{obj.user.name} {obj.user.surname}'

    class Meta:
        model = Team
        fields = [
            'id',
            'user',
            'name',
            'occupied_places',
            'places',
            'creation_date',
            'leader'
        ]


class MembersSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    team = serializers.ReadOnlyField(source='team.id')
    member = serializers.SerializerMethodField()

    def get_member(self, obj):
        return f'{obj.user.name} {obj.user.surname}'

    class Meta:
        model = Members
        fields = [
            'id',
            'user',
            'team',
            'member'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.id')

    class Meta:
        model = Project
        fields = [
            'id',
            'company',
            'title',
            'description',
            'front',
            'back'
        ]
