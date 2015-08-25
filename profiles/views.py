from polls.models import UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from polls.forms import UserForm, UserProfileForm, UserProfileFormReduced
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

def find_user(request): 
    if not request.user.social_auth.exists():
        candidate = LegacyUser.objects.\
                        filter(name__icontains='{} {}'.format(\
                                request.POST['last_name'],\
                                request.POST['first_name'])\
                               ).\
                        filter(cardnumber__regex=r'^.{14}' + request.POST['cardnumber']) 
        if not candidate.exists():
            return False
        last_name = request.POST['last_name'] 
        first_name = request.POST['first_name']
    else:
        last_name = request.user.last_name 
        first_name = request.user.first_name
    candidate = LegacyDorm.objects.\
                    filter(last_name=last_name).\
                    filter(first_name=first_name).\
                    filter(room=request.POST['room'])
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
    """
     долгое и мучительное обдумывание привело к выводу:\
     candidat, у которых одинаковые firts_name, last_name, cardnumber, считаются одинаковыми по определению

     по сути, проверяем, есть ли вообще подходящие карточки. Если нет, то уже выпилили. Если есть, то неважно, сколько их.\
     Вероятность того, что в базе будет два человека с одинаковыми ФИ и днём рождения, считается малой

     что делать, если в базе несколько человек с одинаковыми ФИ?
     считаем, что их не поселят в одну комнату, иначе ручная обработка 
    """
    user = request.user
    profile = user.userprofile
    if user.social_auth.exists():
        ProfileForm = UserProfileFormReduced
    else:
        ProfileForm = UserProfileForm
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance = user)
        profile_form = ProfileForm(request.POST, instance = profile)
        if profile_form.is_valid() and (user.social_auth.exists() or user_form.is_valid()):
            candidate = find_user(request)
            if candidate:
                if len(candidate) > 1:
                    messages.error(request, 'Поздравляем! Судя по нашим данным, вам очень повезло с соседом.\
                                             Если вы уверены в правильности введённых данных, пишите на \
                                             vote@dgap.mipt.ru, указывая тему письма "Замечательный сосед"')
                elif is_registered(candidate[0].id):
                    messages.error(request, 'Пользователь с такими данными уже зарегистрирован. Если вы уверены\
                                             в правильности введённых данных, пишите на vote@dgap.mipt.ru,\
                                             указывая тему письма "Проблемы при регистрации"')
                else:
                    candidate = candidate[0]
                    if not user.social_auth.exists():
                        user_form.save()
                    profile_form.save()
                    profile.dorm = candidate.id
                    profile.middlename = candidate.middle_name
                    profile.group = candidate.group
                    profile.approval = True 
                    profile.save()
                    messages.success(request, "Регистрация пройдена. Теперь вы можете участвовать в голосовании")
                    return redirect('polls:done')
            else:
                messages.error(request, 'Пользователя, удовлетворяющего введённым данным, в базе не обнаружено. \
                                         Если вы уверены в правильности введённых данных, пишите на vote@dgap.mipt.ru,\
                                         указывая тему письма "Проблемы при регистрации"')
    else:
        user_form = UserForm(instance = user)
        profile_form = ProfileForm(instance = profile)

    mipt = False
    phystech = False
    if user.social_auth.exists():
        if user.social_auth.filter(provider='mipt-oauth2'):
            mipt = user.social_auth.get(provider='mipt-oauth2').uid
        if user.social_auth.filter(provider='google-oauth2'):
            #phystech = user.social_auth.get(provider='google-oauth2').login
            phystech = user.social_auth.get(provider='google-oauth2').uid

    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'mipt': mipt,
        'phystech': phystech,
    })


