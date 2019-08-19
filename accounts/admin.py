from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from import_export.admin import ImportMixin

from accounts.models import User, StudentInfo
from accounts.resources import StudentInfoResource


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = '-date_joined', 'email',
    readonly_fields = 'date_joined', 'last_login',
    list_display = 'email', 'get_short_name', 'group', 'sex', 'room'
    list_filter = 'is_active', 'is_staff', 'is_verified', 'is_superuser', 'sex', 'group',

    search_fields = 'email', 'last_name', 'first_name', 'patronymic',
    filter_horizontal = 'groups', 'user_permissions',

    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'sex',
                                      'group', 'course', 'room', 'is_verified', )}),
        ('Даты', {'fields': ('date_joined', 'last_login', )}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', ),
            'classes': ('wide',),
        }),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'patronymic', 'sex',
                                      'group', 'course', 'room')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )


@admin.register(StudentInfo)
class StudentInfoAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = StudentInfoResource
    list_display = 'get_full_name', 'email', 'vk_url', 'user',
    search_fields = 'email', 'last_name', 'first_name', 'patronymic', 'vk_url',
    raw_id_fields = 'user',
