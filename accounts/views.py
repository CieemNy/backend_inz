from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import F
from .serializers import *
from rest_framework import permissions, status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

User = get_user_model()


# endpoint: display list of users

class UserList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'users-list'


# endpoint: display, edit, delete user details

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
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

class CreateTeam(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = self.request.data
        team = Team.objects.create(
            user=self.request.user,
            name=data['name'],
            access_code=data['access_code'],
            occupied_places=1,
            places=data['places']
        )
        team.save()
        self.request.user.is_leader = True
        self.request.user.is_member = True
        self.request.user.is_madeChoices = False
        self.request.user.save()
        member = Members.objects.create(team=team, user=self.request.user)
        member.save()
        serializer = TeamSerializer(team)
        return Response(serializer.data)


# endpoint: display team
class TeamDetail(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    name = 'team-detail'


# endpoint: list teams

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
        if self.request.user.is_madeChoices:
            return Response("Dokonałeś już wyborów", status.HTTP_403_FORBIDDEN)

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
            request.user.is_madeChoices = True
            request.user.save()
            serializer = TeamChoicesSerializer(team_choices)
            return Response(serializer.data)


# endpoint: display teams choices which are not considered

class TeamsChoices(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = TeamChoices.objects.all().order_by('choice_first', 'choice_second', 'choice_third', 'choice_fourth', 'date').filter(is_considered=False)
    serializer_class = TeamChoicesSerializer
    name = 'team-choices-not-considered'


# endpoint: display teams choices which are considered

class TeamsChoicesConsidered(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = TeamChoices.objects.all().filter(is_considered=True)
    serializer_class = TeamChoicesSerializer
    name = 'team-choices-considered'


# endpoint: display teams choices which are considered

class FinalListTeamsCompanies(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = TeamChoices.objects.all().order_by('final_choice').filter(is_considered=True)
    serializer_class = TeamChoicesSerializer
    name = 'final-list-teams-companies'


# endpoint: display single team choices

class TeamChoicesDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = TeamChoices.objects.all()
    serializer_class = TeamChoicesSerializer
    name = 'team-choices-detail'


# endpoint: display team choices

@api_view(['GET'])
def team_choices(request, pk):
    if request.method == 'GET':
        choices = TeamChoices.objects.all().filter(team=pk)
        serializer = TeamChoicesSerializer(choices, many=True)
        return Response(serializer.data)


class SelectFinalChoice(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def put(self, request, pk):
        data = request.data
        choice = TeamChoices.objects.get(id=pk)
        company = Company.objects.get(id=data['final_choice'])
        if company.occupied_places >= company.places:
            return Response("Brak dostępnych miejsc w wybranej firmie", status.HTTP_403_FORBIDDEN)
        else:
            choice.final_choice = company
            choice.is_considered = True
            choice.save()
            company.occupied_places += 1
            company.save()
            serializer = TeamChoicesSerializer(choice)
            return Response(serializer.data)


# endpoint: display user team choices

class UserTeamChoices(generics.ListAPIView):
    serializer_class = TeamChoicesSerializer
    name = 'user-team-choices'

    def get_queryset(self):
        return TeamChoices.objects.filter(team__members__user=self.request.user)


# endpoint: list companies where are available places

class ListCompanyPlaces(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Company.objects.all().filter(occupied_places__lt=F('places'))
    serializer_class = CompanySerializer
    name = 'company-list-available-places'
