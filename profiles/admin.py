from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from profiles.models import UserProfile, StudentInfo


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            # hide UserProfileInline in the add view
            if isinstance(inline, UserProfileInline) and obj is None:
                continue
            yield inline.get_formset(request, obj), inline

    def get_approved(self, obj):
        return obj.userprofile.is_approved
    get_approved.boolean = True
    get_approved.short_description = 'Подтверждён'
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_approved',]
    list_filter = ['is_staff', 'is_superuser', 'groups', 'is_active', 'get_approved']

class StudentInfoAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'group', 'vk', 'phystech']
# TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user', 'group', 'is_approved']
    list_filter = ['is_subscribed', 'is_approved']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(StudentInfo, StudentInfoAdmin)
