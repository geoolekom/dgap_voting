from profiles.models import UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator


def find_user(request): 
    last_name = request.user.last_name 
    first_name = request.user.first_name
    middle_name = request.user.userprofile.middlename
    candidate = LegacyDorm.objects.\
                    filter(last_name=last_name).\
                    filter(first_name=first_name).\
                    filter(middle_name=middle_name)
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
    profile = user.userprofile
    mipt = False
    phystech = False
    if not profile.is_approved and user.social_auth.exists():
        candidate = find_user(request)
        if candidate:
            if len(candidate) > 1:
                messages.error(request, 'В базе более одного студента с данными ФИО. Пожалуйста, напишите на vote@dgap.mipt.ru, указывая тему письма "Проблемы при регистрации"')
            elif is_registered(candidate[0].id):
                messages.error(request, 'Пользователь с такими данными уже зарегистрирован. Если вы уверены в правильности введённых данных, пишите на vote@dgap.mipt.ru, указывая тему письма "Проблемы при регистрации"')
            else:
                candidate = candidate[0]
                profile.dorm = candidate.id
                profile.group = candidate.group
                profile.room = candidate.room
                profile.is_approved = True 
                profile.save()
                messages.success(request, "Регистрация пройдена. Теперь вы можете участвовать в голосовании")
        else:
            messages.error(request, 'Вы не являетесь студентом или аспирантом ФОПФ. Если вы так не считаете, то пишите на vote@dgap.mipt.ru, указывая тему письма "Проблемы при регистрации"')
    if user.social_auth.exists():
        if user.social_auth.filter(provider='mipt-oauth2'):
            mipt = user.social_auth.get(provider='mipt-oauth2').extra_data['login']
        if user.social_auth.filter(provider='google-oauth2'):
            #phystech = user.social_auth.get(provider='google-oauth2').login
            phystech = user.social_auth.get(provider='google-oauth2').uid

    return render(request, 'profiles/profile.html', {
        'mipt': mipt,
        'phystech': phystech,
    })


