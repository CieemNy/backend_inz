from django.urls import path, include
from . import views
from django.contrib import admin

from .views import JoinTeam

admin.site.site_url = 'http://127.0.0.1:8000/accounts/'
urlpatterns = [
    # user endpoints
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('user/team', views.UserTeam.as_view(), name='user-team'),
    path('user/company', views.UserCompany.as_view(), name='user-company'),
    # company endpoints
    path('company', views.ListCompany.as_view(), name='list-company'),
    path('company/<int:pk>', views.CompanyDetail.as_view(), name='company-detail'),
    path('company/add', views.CreateCompany.as_view(), name='create-company'),
    # teams endpoints
    path('teams', views.ListTeams.as_view(), name='list-team'),
    path('teams/<int:pk>', views.TeamDetail.as_view(), name='team-detail'),
    path('teams/<int:pk>/members', views.team_members, name='team-members'),
    path('teams/<int:pk>/join', JoinTeam.as_view(), name='team-join'),
    path('teams/create', views.CreateTeam.as_view(), name='create-team'),
]
