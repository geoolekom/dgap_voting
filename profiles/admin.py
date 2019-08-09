"""Admin classes for models in :mod:`profiles.models`.

Quite obvious, only custom admin for :class:`django.contrib.auth.models.User` may raise some interest. See source code."""

from django.contrib import admin
from profiles.models import UserProfile, StudentInfo


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class StudentInfoAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'group', 'vk', 'phystech']
    list_filter = ['course']
# TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы


# class StudentInfoInline(admin.StackedInline):
#    model = StudentInfo
#    can_delete = False


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user', 'group', 'is_approved']
    list_filter = ['is_subscribed', 'is_approved']
    # inlines = [StudentInfoInline,]


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
