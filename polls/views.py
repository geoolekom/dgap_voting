from polls.models import Choice, Poll, UserHash
from profiles.models import UserProfile
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from random import randint
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F


import csv
from sendfile import sendfile
import os.path
import subprocess
import logging


maxInt = 2147483647
logger = logging.getLogger('django.request')


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
            polls = [poll for poll in Poll.objects.filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_voted(self.request.user)]

            if self.request.user.is_staff:
                return polls
            else:
                return [poll for poll in polls if not poll.poll_type == Poll.TARGET_LIST or not poll.only_for_staff]
        else:
            return []


class Available(IndexBase):
    def get_context_data(self, *args, **kwargs):
        context = super(Available, self).get_context_data(*args, **kwargs)
        context['target'] = 'available'

        return context

    def get_queryset(self):
        if self.request.user.is_authenticated():
            polls = [poll for poll in Poll.objects.filter(begin_date__lte=timezone.now()).filter(end_date__gte=timezone.now()).order_by('-begin_date') if poll.is_user_target(self.request.user) and not poll.is_user_voted(self.request.user)]

            if self.request.user.is_staff:
                return polls
            else:
                return [poll for poll in polls if not poll.poll_type == Poll.TARGET_LIST or not poll.only_for_staff]
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

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        poll = self.object
        if poll.is_user_voted(self.request.user):
            target = 'voted'
        elif poll.is_user_target(self.request.user) and poll.is_started() and not poll.is_closed():
            target = 'available'
        else:
            target = 'not available'
    #def get_queryset(self):
    #    return Poll.objects.filter(begin_date__lte=timezone.now(), end_date__gte=timezone.now())


class Results(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_queryset(self):
        return Poll.objects.filter(end_date__lte=timezone.now())


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def voters(request, poll_id):
    poll_obj = get_object_or_404(Poll, pk=poll_id)

    if poll_obj.poll_type == Poll.TARGET_LIST:
        raw_people = [voter.student_info for voter in poll_obj.participant_set.all() if voter.student_info]
        people = []
        for item in raw_people:
            if hasattr(item, 'userprofile_set'):
                if item.userprofile_set.all():
                    people.append(item.userprofile_set.all()[0])
    else:
        people = [voter for voter in UserProfile.objects.all().order_by('user__last_name') if voter.is_approved and poll_obj.is_user_target(voter.user)]

    return render(request, 'polls/people.html', {
        'voters': people,
        'voters_num': len(people)
    })


def make_csv(p, filename):
    try:
        with open(filename, 'x') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([p.name])
            writer.writerow([])
            for question in p.question_set.all():
                writer.writerow([question.question])
                writer.writerow(['Вариант ответа', 'Количество голосов'])
                for choice in question.choice_set.all().order_by('-votes'):
                    writer.writerow([choice.choice_text, choice.votes])
                writer.writerow([])
                if p.public:
                    writer.writerow(['Фамилия', 'Имя', 'Отчество', 'Группа', 'Комната', 'Голос'])
                else:
                    writer.writerow(['Ключ', 'Голос'])
                for choice in question.choice_set.all():
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
                if p.poll_type == Poll.TARGET_LIST:
                    for participate in p.participant_set.all():
                        if participate.voted:
                            writer.writerow([participate.user_info.fio])
                else:
                    for user in p.voted_users.order_by('last_name', 'first_name'):
                        writer.writerow(["{} {} {}".format(user.last_name, user.first_name, user.userprofile.middlename )])
    except FileExistsError as e:
        logger.warning(e)
        return False
    else:
        return True


# Convert file to WIN-1251 for windows users
def make_win_csv(oldfilename, filename):
    error = subprocess.call(["iconv", "-t", "WINDOWS-1251", oldfilename, "-o", filename])
    if error:
        logger.warning('"iconv" failed while processing "make_win_csv", see logs to understand')
        return False
    else:
        return True


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
    return sendfile(request, filename, attachment=True, attachment_filename="poll{}.csv".format(poll_id))


def done(request):
    storage = messages.get_messages(request)
    if storage:
        return render(request, 'polls/done.html')
    else:
        return redirect('polls:index')


def vote(request, poll_id):
    if request.method == 'POST':
        p = get_object_or_404(Poll, pk=poll_id, begin_date__lte=timezone.now(), end_date__gte=timezone.now())
        user = request.user
        if not user.is_authenticated():
            messages.error(request, 'Вы не вошли как зарегистрированный пользователь')
            return redirect('polls:detail', pk=poll_id)
        if not user.userprofile.is_approved:
            messages.error(request, 'Вы не являетесь подтверждённым пользователем')
            return redirect('polls:detail', pk=poll_id)
        if p.is_user_voted(user) and not (user.is_staff and settings.DEBUG):
            messages.error(request, 'Вы уже приняли участие в этом голосовании')
            return redirect('polls:detail', pk=poll_id)
        if not p.is_user_target(user):
            messages.error(request, 'Вы не являетесь целевой аудиторией голосования')
            return redirect('polls:detail', pk=poll_id)

        message = 'Ваш голос учтён. Идентификационные ключи, соответствующие вашему выбору:\n'

        for question in p.question_set.all():
            choices = request.POST.getlist('question{}-choice'.format(question.id), False)
            if not choices and question.required:
                messages.error(request, 'Вопрос {} является обязательным. Вы не ответили на него'.format(question.question))
                return redirect('polls:detail', pk=poll_id)
            choices = list(set(choices))

            userHashes = [1] * len(choices)
            if question.answer_type == 'OWN':
                c = question.choice_set.create(choice_text=choices[0], votes=0)
                choices[0] = c.pk
            if question.answer_type != 'MANY':
                if len(choices) > 1:
                    messages.error(request, 'В вопросе {} можно выбрать только один вариант ответа'.format(question.question))
                    return redirect('polls:detail', pk=poll_id)
            for i in range(len(choices)):
                selected_choice = question.choice_set.get(pk=choices[i])
                selected_choice.votes = F('votes') + 1
                selected_choice.save()
                userHashes[i] = UserHash()
                userHashes[i].value = randint(0, maxInt)
                userHashes[i].choice = selected_choice
                message += str(userHashes[i].value) + '\n'
                if p.public:
                    userHashes[i].user = user
                userHashes[i].save()

        if p.poll_type == Poll.TARGET_LIST:
            participate = user.userprofile.student_info.participant_set.all()
            for item in participate:
                if item.poll.id == p.id:
                    item.voted = True
                    item.save()
        else:
            p.voted_users.add(user)

        messages.success(request, message)
        return redirect('polls:voted')
    else:
        return request('polls:available')
