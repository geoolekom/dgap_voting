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
    # link for generating pdf
    def pdf_button(self, obj):
        site_url = Site.objects.get_current().domain
        if not site_url.startswith('http://'):
            site_url = 'http://%s'%site_url
        return mark_safe('<a href=\'' + reverse('polls:create_advert', args=[obj.pk,]) +'\'">Генерировать pdf</a>')
    pdf_button.short_description = 'Создание объявления'
    
    # link for target audience display
    def audit_button(self, obj):
        site_url = Site.objects.get_current().domain
        if not site_url.startswith('http://'):
            site_url = 'http://%s'%site_url
        return mark_safe('<a href=\'' + reverse('polls:people', args=[obj.pk,]) +'\'">Показать список избирателей</a>')
    audit_button.short_description = 'Целевая аудитория'
    
    # link for mailing for those who can vote but hadn't done it yet
    # number in [] shows number of mailings already mage for the poll
    def mailing_button(self, obj):
        times_mailed = obj.times_mailed
        site_url = Site.objects.get_current().domain
        if not site_url.startswith('http://'):
            site_url = 'http://%s'%site_url
        return mark_safe('<a href=\'' + os.path.join(site_url, reverse('polls:approve_mailing', args=[obj.pk,])) +'\'">Сделать рассылку</a> [{times_mailed}]'.format(times_mailed=times_mailed))
    mailing_button.short_description = 'Уведомление о голосовании'
    
    exclude = ('voted_users', 'times_mailed', 'last_mailing',)
    inlines = [ChoiceInline,]
    list_display=['name', 'pdf_button', 'audit_button', 'mailing_button',]

admin.site.register(Poll, PollAdmin)

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
        return obj.userprofile.is_approved()
    get_approved.boolean = True
    get_approved.short_description = 'Подтверждён'
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'get_approved',]

#TODO нормальное отображение профиля юзера в админке, разобраться, нужно ли показывать права доступа и группы 

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

