from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from .models import Issue, Event, EventDocument
from .forms import IssueCreateForm, DeptEventCreateForm, UserEventCreateForm


@method_decorator(login_required, name='dispatch')
class IssueDisplay(generic.DetailView):
    model = Issue

    def get_context_data(self, **kwargs):
        context = super(IssueDisplay, self).get_context_data(**kwargs)
        context['events'] = context["object"].event_set.order_by("add_dttm")
        if self.request.user.is_staff or self.request.user.is_superuser:
            context["form"] = DeptEventCreateForm()
        elif self.request.user == context['object'].author:
            context["form"] = UserEventCreateForm()
        return context


@method_decorator(login_required, name='dispatch')
class UserEventCreate(generic.detail.SingleObjectMixin, generic.FormView):
    template_name = 'senate/issue_detail.html'
    model = Issue

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        self.object = self.get_object()
        return super(UserEventCreate, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('senate:issue_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return DeptEventCreateForm
        return UserEventCreateForm

    def form_valid(self, form):
        print("VALID")
        if self.request.user.is_staff or self.request.user.is_superuser:
            cls, new_status, new_dept = form.cleaned_data["cls"], form.cleaned_data["new_status"], form.cleaned_data["new_dept"]
        else:
            if self.object.author != self.request.user:
                raise PermissionDenied
            cls, new_status, new_dept = Event.UPDATE, None, None
        event = Event.objects.create(issue=self.object,
                                     author=self.request.user,
                                     cls=cls,
                                     info=form.cleaned_data["info"],
                                     new_status=new_status,
                                     new_dept=new_dept)
        for i in range(1, 4):
            photo = form.cleaned_data['photo' + str(i)]
            if photo:
                EventDocument.objects.create(file=photo, event=event)
        messages.add_message(self.request, messages.SUCCESS, "Обращение обновлено")
        return super(UserEventCreate, self).form_valid(form)


class IssueDetail(View):

    def get(self, request, *args, **kwargs):
        view = IssueDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserEventCreate.as_view()
        return view(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class IssueCreate(generic.CreateView):
    model = Issue

    def get_form(self, form_class=None):
        return IssueCreateForm(self.request.GET)

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
class MyIssueList(generic.ListView):
    model = Issue
    template_name = 'senate/issue_list.html'

    def get_queryset(self):
        user = self.request.user
        if user.userprofile.student_info:
            users = [profile.user for profile in user.userprofile.student_info.userprofile_set.all()]
        else:
            users = [user]
        return Issue.objects.filter(author__in=users).order_by("-add_dttm")


@method_decorator(login_required, name='dispatch')
class DeptIssueList(UserPassesTestMixin, generic.ListView):
    model = Issue
    template_name = 'senate/issue_list.html'

    def get_queryset(self):
        user = self.request.user
        groups = user.groups.all()
        return Issue.objects.filter(assigned_dept__in=groups).order_by("-add_dttm")

    def test_func(self):
        # return self.request.user.groups.filter(name="senate_employee").count >= 1
        return self.request.user.is_superuser or self.request.user.is_staff


class FullIssueList(generic.ListView):
    model = Issue
    template_name = 'senate/issue_list.html'

    def get_queryset(self):
        return Issue.objects.all().order_by("-add_dttm")
