from django.contrib import admin
from polls.models import Poll, Choice
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import os
from django.core.urlresolvers import reverse
from polls.models import Participant


class ParticipantInline(admin.TabularInline):
    model = Participant
    exclude = ('user_information', )
    fields = ('voted', )

    list_dispay = ['userprofile']


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
    inlines = [ChoiceInline, ParticipantInline, ]
    list_display=['name', 'pdf_button', 'audit_button', 'mailing_button',]

admin.site.register(Poll, PollAdmin)