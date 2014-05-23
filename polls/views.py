from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from polls.models import Choice, Poll, UserHash
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import re
from random import randint
from django.contrib import messages
from django.utils import timezone

maxInt = 2147483647

class Index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.filter(begin_date__lte=timezone.now()).order_by('-begin_date')[:25]

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
    if user.get_username() != 'admin' and p.voted_users.filter(pk=user.pk).exists():
        messages.error(request, 'Вы уже приняли участие в этом голосовании')
        return redirect('polls:detail', pk=poll_id)
    if not ((re.compile(p.target_room, re.IGNORECASE)).match(user.userprofile.room) and
            (re.compile(p.target_group, re.IGNORECASE)).match(user.userprofile.group)):
        messages.error(request, 'Вы не являетесь целевой аудиторией голосования')
        return redirect('polls:detail', pk=poll_id)
    choices = request.POST.getlist('choice', False)
    if not choices:
        messages.error(request, 'Вы не выбрали вариант ответа')
        return redirect('polls:detail', pk=poll_id)
    p.voted_users.add(user)
    userHashes = [1] * len(choices)
    message = 'Ваш голос учтён. Идентификационные ключи, соответствующие вашему выбору:\n'
    if p.anwer_type == 'OWN':
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
   
