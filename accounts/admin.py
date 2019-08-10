from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = '-date_joined', 'email',
    readonly_fields = 'date_joined', 'last_login',
    list_display = 'email', 'get_short_name', 'group', 'sex', 'room'
    list_filter = 'is_active', 'is_staff', 'is_superuser', 'groups', 'sex', 'group',

    search_fields = 'email', 'last_name', 'first_name', 'patronymic',
    filter_horizontal = 'groups', 'user_permissions',

    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'sex',
                                      'group', 'course', 'room', 'is_verified', )}),
        ('Даты', {'fields': ('date_joined', 'last_login', )}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', ),
            'classes': ('wide',),
        }),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'sex',
                                      'group', 'course', 'room')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', )}),
    )
