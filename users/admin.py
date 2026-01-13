from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email','username','role','is_staff']

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'bio')}),
    )

    add_filedsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields':('email', 'role', 'bio')}), 
    )

admin.site.register(CustomUser, CustomUserAdmin)


