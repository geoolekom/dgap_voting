from .models import AidRequest, AidDocument, get_next_date
from .forms import AidRequestCreateForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from .create_paper import create_paper


@method_decorator(login_required, name='dispatch')
class AidRequestList(generic.ListView):
    # template_name = 'fin_aid/aidrequest_list.html'
    model = AidRequest

    def get_queryset(self):
        user = self.request.user
        if user.userprofile.student_info:
            users = [profile.user for profile in user.userprofile.student_info.userprofile_set.all()]
        else:
            users = [user]
        return AidRequest.objects.filter(applicant__in=users).order_by("-add_dttm")


@method_decorator(login_required, name='dispatch')
class AidRequestCreate(generic.CreateView):
    model = AidRequest
    form_class = AidRequestCreateForm

    def get_success_url(self):
        return reverse('fin_aid:aid_request_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AidRequestCreate, self).get_context_data(**kwargs)
        context['deadline_dt'] = get_next_date(None, 'deadline')
        context['payment_dt'] = get_next_date(None, 'payment')
        print(self.context_object_name)
        return context

    def form_valid(self, form):
        response = super(AidRequestCreate, self).form_valid(form)
        self.object.applicant = self.request.user
        for i in range(1, 4):
            document = form.cleaned_data['document' + str(i)]
            if document:
                AidDocument.objects.create(file=document, request=self.object)
        self.object.save()
        if self.object.applicant.userprofile.is_approved:
            create_paper(self.object)
        messages.add_message(self.request, messages.SUCCESS, "Заявление на матпомощь принято. Результаты рассмотрения"
                                                             " будут доступны в личном кабинете")
        return response


class AidRequestUpdate(generic.UpdateView):
    model = AidRequest
    form_class = AidRequestCreateForm

    def get_success_url(self):
        return reverse('fin_aid:aid_request_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AidRequestUpdate, self).get_context_data(**kwargs)
        context['deadline_dt'] = get_next_date(None, 'deadline')
        context['payment_dt'] = get_next_date(None, 'payment')
        print(self.context_object_name)
        return context

    def form_valid(self, form):
        response = super(AidRequestUpdate, self).form_valid(form)
        self.object.applicant = self.request.user
        for i in range(1, 4):
            document = form.cleaned_data['document' + str(i)]
            if document:
                AidDocument.objects.create(file=document, request=self.object)
        self.object.save()
        if self.object.applicant.userprofile.is_approved:
            create_paper(self.object)
        messages.add_message(self.request, messages.SUCCESS,
                             "Заявление на матпомощь изменено. Результаты рассмотрения"
                             " будут доступны в личном кабинете")
        return response

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        if aid_request.status not in [AidRequest.WAITING, AidRequest.INFO_NEEDED]:
            messages.add_message(self.request, messages.ERROR,
                                 "Заявление уже рассмотрено, Вы не можете изменить его")
            return redirect(reverse_lazy('fin_aid:index'))
        return super(AidRequestUpdate, self).dispatch(request, *args, **kwargs)


class AidRequestDelete(generic.DeleteView):
    model = AidRequest
    success_url = reverse_lazy('fin_aid:aid_request_list')

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        if aid_request.status not in [AidRequest.WAITING, AidRequest.INFO_NEEDED]:
            messages.add_message(self.request, messages.ERROR,
                                 "Заявление уже рассмотрено, Вы не можете удалить его")
            return redirect(reverse_lazy('fin_aid:index'))
        return super(AidRequestDelete, self).dispatch(request, *args, **kwargs)


class AidRequestDetail(generic.DetailView):
    model = AidRequest

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        return super(AidRequestDetail, self).dispatch(request, *args, **kwargs)
