from django.urls import path, include
from . import views
from django.contrib import admin

from .views import JoinTeam, CreateProject, ListCompanyProject, AddTeamChoices, SelectFinalChoice

admin.site.site_url = 'http://127.0.0.1:8000/accounts/'
urlpatterns = [
    # user endpoints
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('user/team', views.UserTeam.as_view(), name='user-team'),
    path('user/company', views.UserCompany.as_view(), name='user-company'),
    path('user/team/choices', views.UserTeamChoices.as_view(), name='user-team-choices'),
    # company endpoints
    path('company', views.ListCompany.as_view(), name='list-company'),
    path('company/places', views.ListCompanyPlaces.as_view(), name='company-list-available-places'),
    path('company/<int:pk>', views.CompanyDetail.as_view(), name='company-detail'),
    path('company/add', views.CreateCompany.as_view(), name='create-company'),
    # teams endpoints
    path('teams', views.ListTeams.as_view(), name='list-team'),
    path('teams/<int:pk>', views.TeamDetail.as_view(), name='team-detail'),
    path('teams/<int:pk>/members', views.team_members, name='team-members'),
    path('teams/<int:pk>/join', JoinTeam.as_view(), name='team-join'),
    path('teams/create', views.CreateTeam.as_view(), name='create-team'),
    # company project endpoints
    path('company/<int:pk>/projects/', ListCompanyProject.as_view(), name='display-projects'),
    path('company/<int:pk>/projects/add', CreateProject.as_view(), name='create-project'),
    # team choices endpoints
    path('teams/<int:pk>/choices/add', AddTeamChoices.as_view(), name='team-choices-add'),
    path('teams/<int:pk>/choices', views.team_choices, name='team-choices'),
    # team choices endpoints: admin
    path('teams/choices', views.TeamsChoices.as_view(), name='teams-choices-not-considered'),
    path('teams/choices/considered', views.TeamsChoicesConsidered.as_view(), name='teams-choices-considered'),
    path('teams/choices/list', views.FinalListTeamsCompanies.as_view(), name='final-list-teams-companies'),
    path('teams/choices/<int:pk>', views.TeamChoicesDetail.as_view(), name='team-choices-details'),
    path('teams/choices/<int:pk>/finalchoice', SelectFinalChoice.as_view(), name='select-team-final-choice'),
]
