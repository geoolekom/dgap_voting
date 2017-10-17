from django.contrib import admin
from polls.models import Poll, Choice
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
import os
from django.core.urlresolvers import reverse
from polls.models import Participant, Question
from nested_inline.admin import NestedTabularInline, NestedModelAdmin


class ParticipantInline(NestedTabularInline):
    model = Participant
    exclude = ('user_information', )
    fields = ('voted', )
    ordering = ('user_information', )

    list_dispay = ['userprofile']


class ChoiceInline(NestedTabularInline):
    model = Choice
    exclude = ('votes',)
    extra = 1


class QuestionInline(NestedTabularInline):
    model = Question
    extra = 1
    inlines = [ChoiceInline]


class PollAdmin(NestedModelAdmin):
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

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.poll_type == Poll.TARGET_LIST and not change:
            obj.create_target_list_from_group_room_course(
                group=obj.target_group,
                room=obj.target_room,
                course=obj.target_course,
                only_staff=obj.only_for_staff
            )
        obj.save()

    exclude = ('voted_users', 'times_mailed', 'last_mailing',)
    inlines = [ParticipantInline, QuestionInline]
    list_display=['name', 'pdf_button', 'audit_button', 'mailing_button',]


class ParticipantAdmin(NestedModelAdmin):
    list_display = ["user_information", "poll", "voted"]
    search_fields = ["user_information__fio"]
    list_editable = ["voted"]
    list_filter = ["voted", "poll"]


admin.site.register(Poll, PollAdmin)
admin.site.register(Participant, ParticipantAdmin)
