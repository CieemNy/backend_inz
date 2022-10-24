from django.contrib import admin

from .models import UserAccount


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_superuser', 'email', 'name', 'surname', 'is_active', 'is_staff', 'is_company', 'is_leader', 'is_member']


admin.site.register(UserAccount, UserAccountAdmin)
