from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from polls.models import Choice, Poll
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic

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

def vote(request, poll_id):
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
         #   'hash': userHash,
        })
