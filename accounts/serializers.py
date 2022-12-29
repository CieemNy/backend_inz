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
            'is_verified',
            'is_ownerCompany',
            'is_madeChoices'
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
            'companyMan',
            'creation_date'
        ]


class TeamSerializer(serializers.ModelSerializer):
    leader = serializers.SerializerMethodField()

    def get_leader(self, obj):
        return f'{obj.user.name} {obj.user.surname}'

    class Meta:
        model = Team
        fields = [
            'id',
            'user',
            'name',
            'access_code',
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
            'back',
            'creation_date'
        ]


class TeamChoicesSerializer(serializers.ModelSerializer):
    first = serializers.SerializerMethodField()
    second = serializers.SerializerMethodField()
    third = serializers.SerializerMethodField()
    fourth = serializers.SerializerMethodField()
    final = serializers.SerializerMethodField()

    def get_first(self, obj):
        return f'{obj.choice_first.name}'

    def get_second(self, obj):
        return f'{obj.choice_second.name}'

    def get_third(self, obj):
        return f'{obj.choice_third.name}'

    def get_fourth(self, obj):
        return f'{obj.choice_fourth.name}'

    def get_final(self, obj):
        return f'{obj.final_choice}'

    class Meta:
        model = TeamChoices
        fields = [
            'id',
            'team',
            'choice_first',
            'choice_second',
            'choice_third',
            'choice_fourth',
            'final_choice',
            'is_considered',
            'date',
            'first',
            'second',
            'third',
            'fourth',
            'final',
        ]
