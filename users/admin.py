from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'first_name', 'phone', 'role', 'is_active', 'is_staff']
    list_filter = ('is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'phone', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'phone', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
    search_fields = ('email', 'first_name', 'phone')
    ordering = ('email',)
