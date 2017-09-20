from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from .models import Issue, Event, EventDocument
from .forms import IssueCreateForm


@method_decorator(login_required, name='dispatch')
class IssueDetail(generic.DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        context['events'] = context["object"].event_set.order_by("add_dttm")
        return context


@method_decorator(login_required, name='dispatch')
class IssueCreate(generic.CreateView):
    model = Issue
    form_class = IssueCreateForm

    def get_success_url(self):
        return reverse('senate:issue_detail', args=(self.object.id,))

    def form_valid(self, form):
        response = super(IssueCreate, self).form_valid(form)
        assigned_dept = self.object.category.department
        self.object.author = self.request.user
        self.object.assigned_dept=assigned_dept
        self.object.save()
        event_info = form.cleaned_data["issue_descr"]
        opening_event = Event.objects.create(issue=self.object,
                                             author=self.request.user,
                                             cls=Event.OPEN,
                                             info=event_info,
                                             new_dept=assigned_dept)

        for i in range(1, 4):
            photo = form.cleaned_data['photo' + str(i)]
            if photo:
                EventDocument.objects.create(file=photo, event=opening_event)
        messages.add_message(self.request, messages.SUCCESS, "Ваше обращение принято. За результатами рассмотрения "
                                                             "следите на сайте")
        return response


@method_decorator(login_required, name='dispatch')
class IssueList(generic.ListView):
    models = Issue

    def get_queryset(self):
        user = self.request.user
        if user.userprofile.student_info:
            users = [profile.user for profile in user.userprofile.student_info.userprofile_set.all()]
        else:
            users = [user]
        return Issue.objects.filter(author__in=users).order_by("-add_dttm")
