from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from polls.models import Choice, Poll, UserHash, UserProfile, LegacyUser, LegacyDorm
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import re
from random import randint
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from polls.forms import UserForm, UserProfileForm, UserProfileFormReduced
import csv
from sendfile import sendfile
import os.path
from django.conf import settings
import subprocess
from django_bleach.models import BleachField
import pyqrcode

maxInt = 2147483647

def check_user(request): 
    if not request.user.social_auth.exists():
        candidat = LegacyUser.objects.filter(name__icontains='{} {}'.format(request.POST['last_name'], request.POST['first_name'])).filter(cardnumber__regex=r'^.{14}' + request.POST['cardnumber']) 
        if not candidat.exists():
            return False
        last_name = request.POST['last_name'] 
        first_name = request.POST['first_name']
    else:
        last_name = request.user.last_name 
        first_name = request.user.first_name
    dorm = LegacyDorm.objects.filter(last_name=last_name).filter(first_name=first_name).filter(room=request.POST['room'])
    if not dorm.exists():
        return False
    return dorm

def check_dorm(id):
    return UserProfile.objects.filter(dorm=id).exists()

def profile_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if request.user.social_auth.exists():
            profile_form = UserProfileFormReduced(request.POST, instance=request.user.userprofile)
        else:
            profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid() and (request.user.social_auth.exists() or user_form.is_valid()):
            dorm = check_user(request)
            if dorm:
#DONE тут уже надо нормально разобраться с кучей карточек и людьми с одинаковыми именами и фамилиями одновременно
# долгое и мучительное обдумывание привело к выводу: candidat, у которых одинаковые firts_name, last_name, cardnumber, считаются одинаковыми по определению
# по сути, проверяем, есть ли вообще подходящие карточки. Если нет, то уже выпилили. Если есть, то неважно, сколько их. Вероятность того, что в базе будет два человека с одинаковыми ФИ и днём рождения, считается малой


# что делать, если в базе несколько человек с одинаовыми ФИ?
# считаем, что их не поселят в одну комнату, иначе ручная обработка 

                if len(dorm) > 1:
                    messages.error(request, 'Поздравляем! Судя по нашим данным, вам очень повезло с соседом. Если вы уверены в правильности введённых данных, пишите на vote@dgap.mipt.ru, указывая тему письма "Замечательный сосед"')
                elif check_dorm(dorm[0].id):
                    messages.error(request, 'Пользователь с такими данными уже зарегистрирован. Если вы уверены в правильности введённых данных, пишите на vote@dgap.mipt.ru, указывая тему письма "Проблемы при регистрации"')
                else:
                    dorm = dorm[0]
                    if not request.user.social_auth.exists():
                        user_form.save()
                    profile_form.save()
                    request.user.userprofile.dorm = dorm.id
                    request.user.userprofile.middlename = dorm.middle_name
                    #request.user.userprofile.room = dorm.room
                    request.user.userprofile.group = dorm.group
                    request.user.userprofile.approval = True 
                    request.user.userprofile.save()
                    messages.success(request, "Регистрация пройдена. Теперь вы можете участвовать в голосовании")
                    return redirect('polls:done')
            else:
                messages.error(request, 'Пользователя, удовлетворяющего введённым данным, в базе не обнаружено. Если вы уверены в правильности введённых данных, пишите на vote@dgap.mipt.ru, указывая тему письма "Проблемы при регистрации"')
    else:
        user_form = UserForm(instance = request.user)
        if request.user.social_auth.exists():
            profile_form = UserProfileFormReduced(instance = request.user.userprofile)
        else:
            profile_form = UserProfileForm(instance = request.user.userprofile)

    return render(request, 'polls/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
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

class Closed(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Closed, self).get_context_data(*args, **kwargs)
        context['target'] = 'closed'
        return context 

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now()).order_by('-end_date')[:12]

class Voted(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Voted, self).get_context_data(*args, **kwargs)
        context['target'] = 'voted'
        return context 

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [poll for poll in Poll.objects.filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_voted(self.request.user)][:12]
        else:
            return []

class Available(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Available, self).get_context_data(*args, **kwargs)
        context['target'] = 'available'
        return context 

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return [poll for poll in Poll.objects.filter(begin_date__lte=timezone.now()).filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_target(self.request.user) and not poll.is_user_voted(self.request.user)][:12]
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
    
    def get_queryset(self):
        return Poll.objects.filter(begin_date__lte=timezone.now(), end_date__gte=timezone.now())

class Results(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now())

def make_html_advert(request, poll_id):
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    qrcode_addr = os.path.join(settings.SENDFILE_ROOT, "qrcode{}.png".format(poll_id))
    
    try:
        qr = pyqrcode.create(request.build_absolute_uri(reverse('polls:detail', args=[poll_id,])))
        qr.png(qrcode_addr, scale=6)
    except ErrorType:
        pass
    
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

def make_pdf_error(request, poll_id, e):
    message = "Невозможно сгенерировать объявление. При повторном возникновении проблемы обратитесь к администратору."
    messages.warning(request, message)
    return redirect('polls:done')

def make_pdf(request, poll_id):
    try:
        poll_obj = get_object_or_404(Poll, pk=poll_id)
        filename = os.path.join(settings.SENDFILE_ROOT, "poll{}".format(poll_id)) 
        html_filename = "{}.html".format(filename)
        pdf_filename = "{}.pdf".format(filename)
        
        with open(html_filename, 'w') as htmlfile:
            htmlfile.write(make_html_advert(request, poll_id))
        
        if not html_to_pdf(html_filename, pdf_filename):
            raise Exception("Something wrong with wkhtmltopdf")
        return sendfile(request, pdf_filename, attachment=True, attachment_filename="{}.pdf".format(poll_obj.name))
        #message = "Объявление успешно создано, ожидайте загрузки"
        #messages.success(request, message)
        #return redirect('polls:done')
    except ErrorType as e:
        return make_pdf_error(request, poll_id, e)

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
    except FileExistsError:
        return False
    else: 
        return True

def make_win_csv(oldfilename, filename):
    error = subprocess.call(["iconv", "-t", "WINDOWS-1251", oldfilename, "-o", filename])
    if error:
        return False
    else:
        return True
    
def voters(request, poll_id):
    poll_obj = get_object_or_404(Poll, pk=poll_id)
    people = [voter for voter in UserProfile.objects.all().order_by('user__last_name') if voter.approval and poll_obj.is_user_target(voter.user)]
    
    return render(request, 'polls/people.html', {
        'voters': people,
        'voters_num': len(people)
    })

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
    p = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    if not user.is_authenticated():
        messages.error(request, 'Вы не вошли как зарегистрированный пользователь')
        return redirect('polls:detail', pk=poll_id)
    if not user.userprofile.approval:
        messages.error(request, 'Вы не являетесь подтверждённым пользователем')
        return redirect('polls:detail', pk=poll_id)
    if user.get_username() != 'admin' and p.is_user_voted(user):
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
   
