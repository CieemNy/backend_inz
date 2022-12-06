from django.contrib import admin

from .models import UserAccount, Company, Team, Members, Project


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_superuser', 'is_staff', 'email', 'name', 'surname', 'is_active', 'is_verified', 'is_company', 'is_leader', 'is_member']
    list_editable = ['is_verified', 'is_company', 'is_leader', 'is_member']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'description', 'contact_number', 'contact_email', 'occupied_places', 'places']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'occupied_places', 'places', 'creation_date']


class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'team']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'title', 'description', 'front', 'back']


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Members, MembersAdmin)
admin.site.register(Project, ProjectAdmin)
