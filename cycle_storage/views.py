from cycle_storage.models import Bicycle, Storage, Place
from cycle_storage.forms import BicycleCreateForm
from django.views import generic
from django.shortcuts import redirect, get_object_or_404


class BicycleDetail(generic.DetailView):
    model = Bicycle


def index_view(request):
    if Bicycle.objects.filter(owner=request.user.userprofile).count() > 0:
        return redirect('bicycle:bicycle_my')
    return redirect('bicycle:bicycle_create')


# TODO multiple bikes?
# TODO error if no bike, should be redirect to bicycle_create
class MyBicycleDetail(generic.DetailView):
    model = Bicycle
    template = "bicycle/bicycle_detail.html"

    def get_object(self):
        return get_object_or_404(Bicycle, owner=self.request.user.userprofile)
        # return Bicycle.objects.get(owner=self.request.user.userprofile)


# TODO unique file names
# TODO bug when passing photo
class BicycleCreate(generic.CreateView):
    model = Bicycle
    form_class = BicycleCreateForm
    success_url = '/bicycle'

    """def get_initial(self):
        initial = super(BicycleCreate, self).get_initial()
        initial['owner'] = self.request.user.userprofile
        return initial"""

    def form_valid(self, form):
        self.object.owner = self.request.user.userprofile
        self.object.save()
        response = super(BicycleCreate, self).form_valid(form)
        return response
