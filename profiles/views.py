"""Currently uses only one template - ``profiles/profile.html``"""

from django.core.exceptions import MultipleObjectsReturned

from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from profiles.models import StudentInfo


class UserChangeEmail(UpdateView):
    """Legacy function for changing user email. Currently not used"""
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
    """Subscribe/unsubscrube from notifications.

    ``request.user.userprofile.is_subscribed = not request.user.userprofile.is_subscribed``
    """
    profile = request.user.userprofile
    profile.is_subscribed = not profile.is_subscribed
    profile.save()
    if profile.is_subscribed:
        messages.success(request, 'Вы подписаны на рассылку')
    else:
        messages.success(request, 'Вы больше не подписаны на рассылку')
    return redirect('index')


@login_required
def profile_view(request):
    """Super old and super shitty view displaying info about current user. Looks like a bit of refactoring needed.

    * Adds error messages if user is not approved & so on.
    * Sets context variables with user's social services logins
    * Renders template ``profiles/profile.html``
    """
    user = request.user
    mipt = False
    phystech = False
    vk = None
    if user.social_auth.exists():
        if user.social_auth.filter(provider='google-oauth2'):
            student_infos = StudentInfo.objects.filter(phystech__iexact=user.email)
            if len(student_infos) == 1:
                if not user.userprofile.is_approved:
                    messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите администраторам сайта')
            elif len(student_infos) < 1:
                messages.error(request, 'Вы не прошли автоматическую верификацию, пишите администраторам сайта')
            else:
                messages.error(request, 'В базе более одного студента с данной почтой. Вы можете попробовать авторизоваться через vk или напишите администраторам сайта')
            phystech = user.social_auth.get(provider='google-oauth2').uid
        elif user.social_auth.filter(provider='vk-oauth2'):
            student_infos = StudentInfo.objects.filter(vk='https://vk.com/' + user.username)
            if len(student_infos) == 1:
                if user.userprofile.is_approved:
                    phystech = user.userprofile.student_info.phystech
                else:
                    messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите администраторам сайта')
            elif len(student_infos) < 1:
                messages.error(request, 'Вы не прошли автоматическую верификацию, пишите администраторам сайта')
                messages.error(request, 'В базе более одного студента с данным профилем VK. Вы можете попробовать авторизоваться через phystech.edu или напишите администраторам сайта')
            vk = user.social_auth.get(provider='vk-oauth2').uid
        else:
            messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите администраторам сайта')

    return render(request, 'profiles/profile.html', {
        'mipt': mipt,
        'phystech': phystech,
        'vk': vk,
    })
