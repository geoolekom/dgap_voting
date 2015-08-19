from django.template import RequestContext, loader
from polls.models import Choice, Poll, UserHash, UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
import re
from random import randint
from django.contrib import messages
from django.utils import timezone
from polls.forms import UserForm, UserProfileForm, UserProfileFormReduced
import csv
from sendfile import sendfile
import os.path
from django.conf import settings
import subprocess
from django_bleach.models import BleachField
import pyqrcode
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
import logging

maxInt = 2147483647
logger = logging.getLogger('django.request')

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
    template_name = 'polls/user_change_email.html'
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

    return render(request, 'polls/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'mipt': mipt,
        'phystech': phystech,
    })

def server_time(request):
    return render(request, 'polls/servertime.html')

def server_timezone(request):
    return render(request, 'polls/servertimezone.html')

def server_date(request):
    return render(request, 'polls/serverdate.html')

class IndexBase(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'poll_list'
    paginate_by = 10

class Closed(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Closed, self).get_context_data(*args, **kwargs)
        context['target'] = 'closed'
        return context 

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now()).order_by('-end_date')

class Voted(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Voted, self).get_context_data(*args, **kwargs)
        context['target'] = 'voted'
        return context 

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [poll for poll in Poll.objects.filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_voted(self.request.user)]
        else:
            return []

class Available(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Available, self).get_context_data(*args, **kwargs)
        context['target'] = 'available'
        return context 

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [poll for poll in Poll.objects.filter(begin_date__lte=timezone.now()).filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_target(self.request.user) and not poll.is_user_voted(self.request.user)]
        else:
            return []

class Index(Closed, Available):
    def get_context_data(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return Available.get_context_data(self, *args, **kwargs)
        else:
            return Closed.get_context_data(self, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Available.get_queryset(self)
        else:
            return Closed.get_queryset(self)

class Detail(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    
    #def get_queryset(self):
    #    return Poll.objects.filter(begin_date__lte=timezone.now(), end_date__gte=timezone.now())

class Results(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now())

def make_html_advert(request, poll_id, poll_obj):
    qrcode_addr = os.path.join(settings.SENDFILE_ROOT, "qrcode{}.png".format(poll_id))
    
    try:
        qr = pyqrcode.create(request.build_absolute_uri(reverse('polls:detail', args=[poll_id,])))
        qr.png(qrcode_addr, scale=6)
    except Exception as e:
        logger.warning(e)
    
    return loader.render_to_string('polls/advert.html', {
        'poll_obj': poll_obj,
        'filename': 'adv_html',
        'main_text': request.POST['main_text'],
        'author_name': request.POST['author_name'],
        'poll_address': request.build_absolute_uri(reverse('polls:detail', args=[poll_id,])),
        'site_name': request.get_host(),
        'qrcode_addr': qrcode_addr
    }, RequestContext(request))

def create_advert(request, poll_id):
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/create_advert.html', {
        'poll_id': poll_id,
        'allowed_tags': settings.BLEACH_ALLOWED_TAGS,
        'allowed_attrs': settings.BLEACH_ALLOWED_ATTRIBUTES,
        'allowed_styles': settings.BLEACH_ALLOWED_STYLES
    })

def html_to_pdf(html_filename, pdf_filename):
    error = subprocess.call(["wkhtmltopdf", "--minimum-font-size", "18", "--margin-top", "25mm", "--margin-bottom", "25mm", "--margin-left", "20mm", "--margin-right", "20mm", html_filename, pdf_filename])
    return not error  

def make_pdf(request, poll_id):
    try:
        poll_obj = get_object_or_404(Poll, pk=poll_id)
        filename = os.path.join(settings.SENDFILE_ROOT, "poll{}".format(poll_id)) 
        html_filename = "{}.html".format(filename)
        pdf_filename = "{}.pdf".format(filename)
        
        with open(html_filename, 'w') as htmlfile:
            htmlfile.write(make_html_advert(request, poll_id, poll_obj))
        
        if not html_to_pdf(html_filename, pdf_filename):
            raise Exception("Something is wrong with wkhtmltopdf, see logs to understand")
        return sendfile(request, pdf_filename, attachment=True, attachment_filename="{}.pdf".format(poll_obj.name))
    except Exception as e: 
        logger.warning(e)
        message = "Невозможно сгенерировать объявление. При повторном возникновении проблемы обратитесь к администратору."
    messages.warning(request, message)
    return redirect('polls:done')

def make_csv(p, filename):
    try:
        with open(filename, 'x') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([p.name])
            writer.writerow([])
            writer.writerow(['Вариант ответа', 'Количество голосов'])
            for choice in p.choice_set.all().order_by('-votes'):
                writer.writerow([choice.choice_text, choice.votes])
            writer.writerow([])
            if p.public:
                writer.writerow(['Фамилия', 'Имя', 'Отчество', 'Группа', 'Комната', 'Голос'])
            else:
                writer.writerow(['Ключ', 'Голос'])
            for choice in p.choice_set.all():
                for user_hash in choice.userhash_set.order_by('value'):
                    if p.public:
                        writer.writerow([
                            user_hash.user.last_name, 
                            user_hash.user.first_name, 
                            user_hash.user.userprofile.middlename,
                            user_hash.user.userprofile.group,
                            user_hash.user.userprofile.room,
                            choice.choice_text
                            ])
                    else:
                        writer.writerow([
                            user_hash.value,
                            choice.choice_text
                            ])
            if not p.public:
                writer.writerow([])
                writer.writerow(["Участники"])
                for user in p.voted_users.order_by('last_name', 'first_name'):
                    writer.writerow(["{} {} {}".format(user.last_name, user.first_name, user.userprofile.middlename )])
    except FileExistsError as e:
        logger.warning(e)
        return False
    else: 
        return True

def make_win_csv(oldfilename, filename):
    error = subprocess.call(["iconv", "-t", "WINDOWS-1251", oldfilename, "-o", filename])
    if error:
        logger.warning('"iconv" failed while processing "make_win_csv", see logs to understand')
        return False
    else:
        return True


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def voters(request, poll_id):   
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    
    people = [voter for voter in UserProfile.objects.all().order_by('user__last_name') if voter.approval and poll_obj.is_user_target(voter.user)]
    
    return render(request, 'polls/people.html', {
        'voters': people,
        'voters_num': len(people)
    })


@login_required
@user_passes_test(is_staff)
def approve_mailing(request, poll_id):    
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    recipients = [profile.user for profile in UserProfile.objects.filter(is_subscribed=True) if profile.is_approved() and poll_obj.is_user_target(profile.user) and not poll_obj.is_user_voted(profile.user)]
    
    return render(request, 'polls/mailing_confirm.html', {
        'poll_id': poll_id,
        'poll': poll_obj,
        'addr_num': len(recipients)
    })


@login_required
@user_passes_test(is_staff)
def mail_unvoted(request, poll_id):    
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    
    call_command('mailing_unvoted', poll_id)
    
    poll_obj.last_mailing = timezone.now()
    poll_obj.times_mailed += 1
    poll_obj.save()
    
    message = "Рассылка успешно произведена"
    messages.info(request, message)
    return redirect('admin:polls_poll_changelist')

def detailed(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id, end_date__lte=timezone.now())
    filename = os.path.join(settings.SENDFILE_ROOT, "poll{}.csv".format(poll_id))
    if not os.path.isfile(filename):
        if not make_csv(p, filename):
            message = "Результаты недоступны в данный момент, попробуйте позже."
            messages.warning(request, message)
            return redirect('polls:done')
    if 'Windows' in request.user_agent.os.family or 'windows' in request.user_agent.os.family:
        oldfilename = filename
        filename = os.path.join(settings.SENDFILE_ROOT, "poll{}win.csv".format(poll_id))
        if not os.path.isfile(filename):
            if not make_win_csv(oldfilename, filename):
                message = "Результаты недоступны в данный момент, попробуйте позже."
                messages.warning(request, message)
                return redirect('polls:done')
    return sendfile(request, filename, attachment=True, attachment_filename="{}.csv".format(p.name))

def done(request):
    storage = messages.get_messages(request)
    if storage:
        return render(request, 'polls/done.html')
    else:
        return redirect('polls:index')

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id, begin_date__lte=timezone.now(), end_date__gte=timezone.now())
    user = request.user
    if not user.is_authenticated():
        messages.error(request, 'Вы не вошли как зарегистрированный пользователь')
        return redirect('polls:detail', pk=poll_id)
    if not user.userprofile.approval:
        messages.error(request, 'Вы не являетесь подтверждённым пользователем')
        return redirect('polls:detail', pk=poll_id)
    if p.is_user_voted(user) and not (user.is_staff and settings.DEBUG):
        messages.error(request, 'Вы уже приняли участие в этом голосовании')
        return redirect('polls:detail', pk=poll_id)
    if not p.is_user_target(user):
        messages.error(request, 'Вы не являетесь целевой аудиторией голосования')
        return redirect('polls:detail', pk=poll_id)
    choices = request.POST.getlist('choice', False)
    if not choices:
        messages.error(request, 'Вы не выбрали вариант ответа')
        return redirect('polls:detail', pk=poll_id)
    p.voted_users.add(user)
    userHashes = [1] * len(choices)
    message = 'Ваш голос учтён. Идентификационные ключи, соответствующие вашему выбору:\n'
    if p.answer_type == 'OWN':
        c = p.choice_set.create(choice_text=choices[0], votes = 0)
        choices[0] = c.pk
    for i in range(len(choices)):
        selected_choice = p.choice_set.get(pk=choices[i])
        selected_choice.votes += 1
        selected_choice.save()
        userHashes[i] = UserHash()
        userHashes[i].value = randint(0, maxInt)
        userHashes[i].choice = selected_choice
        message += str(userHashes[i].value) + '\n'
        if p.public:
            userHashes[i].user = user
        userHashes[i].save()
    messages.success(request, message)
    return redirect('polls:done')
   
