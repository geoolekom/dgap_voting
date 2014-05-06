from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from polls.models import Poll, Choice, UserProfile

class ChoiceInline(admin.TabularInline):
    model = Choice
    exclude = ('votes',)
    extra = 1

class PollAdmin(admin.ModelAdmin):
    exclude = ('voted_users',)
    inlines = [ChoiceInline,]

admin.site.register(Poll, PollAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

#TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

