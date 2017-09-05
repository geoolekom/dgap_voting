from cycle_storage.models import Bicycle, Storage, Place
from cycle_storage.forms import BicycleCreateForm
from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied


class BicycleDetail(generic.DetailView):
    model = Bicycle


def has_bike(user):
    return user.is_authenticated() and Bicycle.objects.filter(owner=user.userprofile).count() > 0


def index_view(request):
    if not request.user.is_authenticated():
        raise PermissionDenied
    if has_bike(request.user):
        return redirect('bicycle:bicycle_my')
    return redirect('bicycle:bicycle_create')


class MyBicycleDetail(generic.DetailView):
    model = Bicycle
    template = "bicycle/bicycle_detail.html"

    def dispatch(self, request, *args, **kwargs):
        # check if there is some video onsite
        if not has_bike(request.user):
            return redirect('bicycle:bicycle_create')
        else:
            return super(MyBicycleDetail, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Bicycle, owner=self.request.user.userprofile)
        # return Bicycle.objects.get(owner=self.request.user.userprofile)


class BicycleCreate(generic.CreateView):
    model = Bicycle
    form_class = BicycleCreateForm
    success_url = '/bicycle'

    def dispatch(self, request, *args, **kwargs):
        if has_bike(request.user):
            return redirect('bicycle:bicycle_my')
        else:
            return super(BicycleCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(BicycleCreate, self).form_valid(form)
        self.object.owner = self.request.user.userprofile
        self.object.save()
        return response
# TODO add ability to cancel storage request
