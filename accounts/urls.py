from django.urls import path, include
from . import views
from django.contrib import admin

admin.site.site_url = 'http://127.0.0.1:8000/accounts/'
urlpatterns = [
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('company', views.CreateCompany.as_view(), name='create-company'),
]
