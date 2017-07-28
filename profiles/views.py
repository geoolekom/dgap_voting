from django.core.exceptions import MultipleObjectsReturned

from profiles.models import UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from profiles.models import UserInformation


def find_user(request): 
    last_name = request.user.last_name 
    first_name = request.user.first_name
    middle_name = request.user.userprofile.middlename
    if middle_name:
        candidate = LegacyDorm.objects.\
                    filter(last_name=last_name).\
                    filter(first_name=first_name).\
                    filter(middle_name=middle_name)
    else:
        candidate = LegacyDorm.objects.\
                    filter(last_name=last_name).\
                    filter(first_name=first_name)
    if not candidate.exists():
        return False
    return candidate


def is_registered(id):
    return UserProfile.objects.filter(dorm=id).exists()


class UserChangeEmail(UpdateView):
    model = User
    fields = ['email']
    template_name = 'profiles/user_change_email.html'
    success_url = reverse_lazy('polls:done')

    def form_valid(self, form):
        messages.success(self.request, "Ваш email был успешно изменён")
        return super(UserChangeEmail, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        return self.request.user

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserChangeEmail, self).dispatch(*args, **kwargs)


@login_required
def change_subscribing_status(request):
    profile = request.user.userprofile
    profile.is_subscribed = not profile.is_subscribed
    profile.save()
    if profile.is_subscribed:
        messages.success(request, 'Вы подписаны на рассылку')
    else:
        messages.success(request, 'Вы больше не подписаны на рассылку')
    return redirect('polls:done')


@login_required
def profile_view(request):
    user = request.user
    mipt = False
    phystech = False
    vk = None
    if user.social_auth.exists():
        if user.social_auth.filter(provider='google-oauth2'):
            user_informations = UserInformation.objects.filter(phystech__iexact=user.email)
            if len(user_informations) == 1:
                if not user.userprofile.is_approved:
                    messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите организатору голосования')
            elif len(user_informations) < 1:
                messages.error(request, 'Вы не прошли автоматическую верификацию, пишите организатору голосования')
            else:
                messages.error(request, 'В базе более одного студента с данной почтой. Вы можете попробовать авторизоваться через vk или напишите организатору голосования')
            phystech = user.social_auth.get(provider='google-oauth2').uid
        elif user.social_auth.filter(provider='vk-oauth2'):
            user_informations = UserInformation.objects.filter(vk='https://vk.com/' + user.username)
            if len(user_informations) == 1:
                if user.userprofile.is_approved:
                    phystech = user.userprofile.user_information.phystech
                else:
                    messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите организатору голосования')
            elif len(user_informations) < 1:
                messages.error(request, 'Вы не прошли автоматическую верификацию, пишите организатору голосования"')
                messages.error(request, 'В базе более одного студента с данным профилем VK. Вы можете попробовать авторизоваться через phystech.edu или напишите организатору голосования')
            vk = user.social_auth.get(provider='vk-oauth2').uid
        else:
            messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите организатору голосования')

    return render(request, 'profiles/profile.html', {
        'mipt': mipt,
        'phystech': phystech,
        'vk' : vk,
    })


