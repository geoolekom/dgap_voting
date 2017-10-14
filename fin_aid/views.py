from django.views.generic import DetailView, ListView, DeleteView
from django.views.generic.edit import FormMixin, ModelFormMixin, BaseCreateView, BaseUpdateView, ProcessFormView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import SingleObjectTemplateResponseMixin, SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator

from sendfile import sendfile

import os
import logging

from polls.views import make_win_csv

from core.settings import MEDIA_ROOT, BASE_DIR, SENDFILE_ROOT
from .models import AidRequest, AidDocument, get_next_date, is_image
from .forms import AidRequestCreateForm
from .create_paper import create_paper

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class AidRequestList(ListView):
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
class AidRequestCreateUpdate(SuccessMessageMixin, SingleObjectTemplateResponseMixin, TemplateResponseMixin,
                             ModelFormMixin, FormMixin, SingleObjectMixin, ProcessFormView, View):
    model = AidRequest
    form_class = AidRequestCreateForm
    template_name = 'fin_aid/aidrequest_form.html'

    def get_success_url(self):
        return reverse('fin_aid:aid_request_detail', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(AidRequestCreateUpdate, self).get_context_data(**kwargs)
        context['student_deadline_dt'] = get_next_date(None, 'student_deadline')
        context['payment_dt'] = get_next_date(get_next_date(None, 'student_deadline'), 'payment')
        return context

    def form_valid(self, form):
        response = super(AidRequestCreateUpdate, self).form_valid(form)
        self.object.applicant = self.request.user
        for i in range(1, 4):
            document = form.cleaned_data['document' + str(i)]
            if document:
                AidDocument.objects.create(file=document, request=self.object, is_image=is_image(document))
        self.object.save()
        if self.object.applicant.userprofile.is_approved:
            try:
                AidDocument.objects.filter(request=self.object, is_application_paper=True).delete()
                create_paper(self.object)
            except Exception as e:
                logger.exception(e, exc_info=True, extra={'request': self.request})

        return response


class AidRequestCreate(AidRequestCreateUpdate, BaseCreateView):
    success_message = "Заявление на матпомощь принято. Результаты рассмотрения будут доступны в личном кабинете"


class AidRequestUpdate(AidRequestCreateUpdate, BaseUpdateView):
    success_message = "Заявление на матпомощь изменено. Результаты рассмотрения будут доступны в личном кабинете"

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        if aid_request.status not in [AidRequest.WAITING, AidRequest.INFO_NEEDED]:
            messages.error(self.request, "Заявление уже рассмотрено, Вы не можете изменить его")
            return redirect(reverse_lazy('fin_aid:index'))
        return super(AidRequestUpdate, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class AidRequestDelete(DeleteView):
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


@method_decorator(login_required, name='dispatch')
class AidRequestDetail(DetailView):
    model = AidRequest

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        return super(AidRequestDetail, self).dispatch(request, *args, **kwargs)


# TODO rewrite
def export_aid_request(request, month=None):
    if not request.user.is_authenticated or (not request.user.groups.filter(name="finance").exists() and not request.user.is_superuser):
        raise PermissionDenied
    if not month:
        month = timezone.now().month
    filename = os.path.join(SENDFILE_ROOT, "export_{}.csv".format(month))
    AidRequest.to_csv(filename, month)
    if 'Windows' in request.user_agent.os.family or 'windows' in request.user_agent.os.family:
        oldfilename, filename = filename, os.path.join(SENDFILE_ROOT, "export_{}_win.csv".format(month))
        if not make_win_csv(oldfilename, filename):
            filename = oldfilename
            logger.warning("Can't change file encoding for Windows")

    return sendfile(request, filename, attachment=True, attachment_filename="export_{}.csv".format(month))
