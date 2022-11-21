from django.contrib import admin

from .models import UserAccount, Company


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_superuser', 'email', 'name', 'surname', 'is_active', 'is_staff', 'is_verified', 'is_company', 'is_leader', 'is_member']
    list_editable = ['is_verified', 'is_company', 'is_leader', 'is_member']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'description', 'contact_number', 'contact_email', 'main_front', 'main_back', 'occupied_places', 'places']


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(Company, CompanyAdmin)
