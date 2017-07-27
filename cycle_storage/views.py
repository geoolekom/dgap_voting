from cycle_storage.models import Bicycle, Storage, Place
from django.views import generic


class BicycleDetail(generic.DetailView):
    model = Bicycle
    template = "cycle_storage/bicycle_detail.html"


# TODO multiple bikes?
class MyBicycleDetail(generic.DetailView):
    model = Bicycle
    template = "cycle_storage/bicycle_detail.html"

    def get_object(self):
        return Bicycle.objects.get(owner=self.request.user.userprofile)

