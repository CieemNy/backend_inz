from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from rest_framework import permissions, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
        self.request.user.is_companyOwner = True
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
        serializer.save(user=self.request.user, occupied_places=1)
        self.request.user.is_leader = True
        self.request.user.is_member = True
        self.request.user.save()
        if serializer.is_valid():
            team = Team.objects.get(pk=serializer.data['id'])
            member = Members.objects.create(team=team, user=self.request.user)
            member.save()


# endpoint: display team
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    name = 'team-detail'


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


# endpoint: display team members

@api_view(['GET'])
def team_members(request, pk):
    if request.method == 'GET':
        members = Members.objects.all().filter(team=pk)
        serializer = MembersSerializer(members, many=True)
        return Response(serializer.data)


class JoinTeam(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        data = self.request.data
        access_code = data['access_code']
        team = Team.objects.get(id=pk)
        if access_code != team.access_code:
            return Response("Nieprawidłowy kod dostępu do teamu", status.HTTP_403_FORBIDDEN)
        if team.occupied_places >= team.places:
            return Response("Brak dostępnych miejsc", status.HTTP_403_FORBIDDEN)
        if self.request.user.is_leader == True or self.request.user.is_member == True or self.request.user.is_company == True:
            return Response("Posiadasz jedną z ról, które uniemozliwiają dołaczenie do zespołu",
                            status.HTTP_403_FORBIDDEN)
        else:
            member = Members.objects.create(
                team=team,
                user=self.request.user,
            )
            serializer = MembersSerializer(member)
            request.user.is_member = True
            request.user.save()
            team.occupied_places += 1
            team.save()
            return Response(serializer.data)


class CreateProject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        company = Company.objects.get(id=pk)
        if company.user != self.request.user:
            return Response("Nie jesteś właścicielem firmy", status.HTTP_403_FORBIDDEN)
        else:
            project_data = request.data
            project = Project.objects.create(
                company=company,
                title=project_data['title'],
                description=project_data['description'],
                front=project_data['front'],
                back=project_data['back']
            )
            serializer = ProjectSerializer(project)
            return Response(serializer.data)


class ListCompanyProject(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        company = Company.objects.get(id=pk)
        projects = Project.objects.filter(company=company)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class AddTeamChoices(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        team = Team.objects.get(id=pk)
        team_choices_data = request.data
        if team.user != self.request.user:
            return Response("Nie jesteś liderem zespołu!", status.HTTP_403_FORBIDDEN)

        elif team.occupied_places != team.places:
            return Response("Twój zespół nie jest skompletowany", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_first'] == team_choices_data['choice_second']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_first'] == team_choices_data['choice_third']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_first'] == team_choices_data['choice_fourth']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_second'] == team_choices_data['choice_third']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_second'] == team_choices_data['choice_fourth']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        elif team_choices_data['choice_third'] == team_choices_data['choice_fourth']:
            return Response("Wybory nie mogą się powtarzać!", status.HTTP_403_FORBIDDEN)

        else:
            team_choices = TeamChoices.objects.create(
                team=team,
                choice_first=Company.objects.get(id=team_choices_data['choice_first']),
                choice_second=Company.objects.get(id=team_choices_data['choice_second']),
                choice_third=Company.objects.get(id=team_choices_data['choice_third']),
                choice_fourth=Company.objects.get(id=team_choices_data['choice_fourth']),
            )
            serializer = TeamChoicesSerializer(team_choices)
            return Response(serializer.data)


class TeamChoicesDetail(generics.RetrieveAPIView):
    queryset = TeamChoices.objects.all()
    serializer_class = TeamChoicesSerializer
    name = 'team-choices-detail'


class TeamsChoices(generics.ListAPIView):
    queryset = TeamChoices.objects.all()
    serializer_class = TeamChoicesSerializer
    name = 'team-choices'
