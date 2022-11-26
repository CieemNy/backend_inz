from django.urls import path, include
from . import views
from django.contrib import admin
from .views import JoinTeam

admin.site.site_url = 'http://127.0.0.1:8000/accounts/'
urlpatterns = [
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('company', views.ListCompany.as_view(), name='list-company'),
    path('company/<int:pk>', views.CompanyDetail.as_view(), name='company-detail'),
    path('company/add', views.CreateCompany.as_view(), name='create-company'),
    path('teams', views.ListTeams.as_view(), name='list-team'),
    path('teams/<int:pk>/join', JoinTeam.as_view(), name='list-team'),
    path('teams/create', views.CreateTeam.as_view(), name='create-team'),
    path('user/team', views.UserTeam.as_view(), name='user-team'),
]
