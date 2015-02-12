from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from polls.models import Poll, Choice, UserProfile
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import os
from django.core.urlresolvers import reverse

class ChoiceInline(admin.TabularInline):
    model = Choice
    exclude = ('votes',)
    extra = 1

class PollAdmin(admin.ModelAdmin):
    # button generating pdf
    def pdf_button(self, obj):
        site_url = Site.objects.get_current().domain
        if not site_url.startswith('http://'):
            site_url = 'http://%s'%site_url
        return mark_safe('<a href=\'' + os.path.join(site_url, reverse('polls:create_advert', args=[obj.pk,])) +'\'">Генерировать pdf</a>')
    pdf_button.short_description = 'Создание объявления'
    
    exclude = ('voted_users',)
    inlines = [ChoiceInline,]
    list_display=['name', 'pdf_button']

admin.site.register(Poll, PollAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

#TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

