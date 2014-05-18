from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from polls.models import Choice, Poll
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
import re

class Index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.order_by('-begin_date')[:25]

class Detail(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

class Results(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

#class Done(generic.DetailView):
#    model = Hash
#    template_name = 'polls/done.html'

def old_vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'polls/done.html', {
         #   'hashes': userHashes,
        })

@login_required(login_url='/polls/')#лучше бы на страницу авторизации
def vote(request, poll_id):
#TODO обработку текстовых ответов
#TODO хэши запилить
    p = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    #return HttpResponse(str(user))
    if p.voted_users.filter(pk=user.pk).exists():
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You have already voted.",
        })
    if user.userprofile.room != p.target_room or user.userprofile.group != p.target_group:
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You haven't permission.",
        })
    choices = request.POST.getlist('choice', False)
    if not choices:
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    p.voted_users.add(user)
    for i in range(len(choices)):
        selected_choice = p.choice_set.get(pk=choices[i])
        selected_choice.votes += 1
        selected_choice.save()
    #всё-таки нужен redirect. Научиться передавать туда данные не через урл
    return render(request, 'polls/done.html', {
         #   'hashes': userHashes,
    })
   
