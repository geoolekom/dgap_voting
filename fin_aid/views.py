from .models import AidRequest, AidDocument
from .forms import AidRequestCreateForm
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


# @method_decorator(login_required, name='dispatch') # newer version of django needed
class AidRequestList(generic.ListView):
    # template_name = 'fin_aid/aidrequest_list.html'
    model = AidRequest

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AidRequestList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return AidRequest.objects.filter(applicant=self.request.user)


# @method_decorator(login_required, name='dispatch')
class AidRequestCreate(generic.CreateView):
    model = AidRequest
    form_class = AidRequestCreateForm
    success_url = '/aid'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AidRequestCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #documents = self.request.FILES.getlist('documents')
        #for document in documents:
        #    doc = AidDocument(document)
        #    doc.save()

        response = super(AidRequestCreate, self).form_valid(form)
        self.object.applicant = self.request.user
        AidDocument.objects.create(file=form.cleaned_data['document'], request=self.object)
        self.object.save()
        return response


class AidRequestDetail(generic.DetailView):
    model = AidRequest

    def dispatch(self, request, *args, **kwargs):
        aid_request = get_object_or_404(AidRequest, pk=self.kwargs['pk'])
        if not aid_request.can_view(request.user):
            raise PermissionDenied
        return super(AidRequestDetail, self).dispatch(request, *args, **kwargs)


