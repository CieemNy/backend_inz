from django.http import HttpResponse
from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


# endpoint: display list of users

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'users-list'


# endpoint: display, edit, delete user details

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'user-detail'

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


# endpoint: create company

class CreateCompany(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    name = 'company-create'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        self.request.user.is_company = True
        self.request.user.save()


# endpoint: list companies

class ListCompany(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-list'


# endpoint: display single company

class CompanyDetail(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    name = 'company-detail'


# endpoint: create team

class CreateTeam(generics.CreateAPIView):
    serializer_class = TeamSerializer
    name = 'team-create'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, occupied_places=+1)
        self.request.user.is_leader = True
        self.request.user.save()
        if serializer.is_valid():
            team = Team.objects.get(pk=serializer.data['id'])
            member = Members.objects.create(team=team, user=self.request.user)
            member.save()


# endpoint: create team

class ListTeams(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    name = 'team-list'


# endpoint: display user team

class UserTeam(generics.ListAPIView):
    serializer_class = TeamSerializer
    name = 'user-team'

    def get_queryset(self):
        return Team.objects.filter(members__user=self.request.user)


# endpoint: display user company

class UserCompany(generics.ListAPIView):
    serializer_class = CompanySerializer
    name = 'user-team'

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


# endpoint: join team

class JoinTeam(APIView):
    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        if team.occupied_places < team.places:
            new_member = Members.objects.create(
                user=self.request.user,
                team=team
            )
            serializer = MembersSerializer(new_member)
            self.request.user.is_member = True
            self.request.user.save()
            team.occupied_places += 1
            team.save()
            return Response(serializer.data)
        if team.occupied_places >= team.places:
            return HttpResponse("brak dostępnych miejsc")
