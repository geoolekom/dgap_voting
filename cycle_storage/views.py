from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from cycle_storage.models import Bicycle, Storage, Place
from cycle_storage.forms import BicycleCreateForm


class BicycleDetail(generic.DetailView):
    model = Bicycle


def has_bike(user):
    return user.is_authenticated() and Bicycle.objects.filter(owner=user).count() > 0


@method_decorator(login_required, name="dispatch")
class MyBicycleDetail(generic.DetailView):
    model = Bicycle
    template = "bicycle/bicycle_detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not has_bike(request.user):
            return redirect('bicycle:bicycle_create')
        else:
            return super(MyBicycleDetail, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Bicycle, owner=self.request.user)


@method_decorator(login_required, name="dispatch")
class BicycleCreate(generic.CreateView):
    model = Bicycle
    form_class = BicycleCreateForm
    success_url = reverse_lazy('bicycle:bicycle_my')

    def dispatch(self, request, *args, **kwargs):
        if has_bike(request.user):
            messages.add_message(self.request, messages.ERROR, "Вы уже зарегистрировали велосипед в системе.")
            return redirect('bicycle:bicycle_my')
        else:
            return super(BicycleCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(BicycleCreate, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, "Заявление принято. Результаты рассмотрения будут доступны в личном кабинете")
        return response


@method_decorator(login_required, name='dispatch')
class BicycleUpdate(generic.UpdateView):
    model = Bicycle
    form_class = BicycleCreateForm
    success_url = reverse_lazy('bicycle:bicycle_my')

    def form_valid(self, form):
        response = super(BicycleUpdate, self).form_valid(form)
        self.object.owner = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS,
                             "Заявление на место в велокомнате изменено. Результаты рассмотрения"
                             " будут доступны в личном кабинете")
        return response

    def dispatch(self, request, *args, **kwargs):
        bicycle = get_object_or_404(Bicycle, pk=self.kwargs['pk'])
        if bicycle.owner != request.user:
            raise PermissionDenied
        if bicycle.request_status not in [Bicycle.WAITING]:
            messages.add_message(self.request, messages.ERROR,
                                 "Заявление уже рассмотрено, Вы не можете изменить его")
            return redirect(reverse_lazy('bicycle:bicycle_my'))
        return super(BicycleUpdate, self).dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class BicycleDelete(generic.DeleteView):
    model = Bicycle
    success_url = reverse_lazy('bicycle:index')

    def dispatch(self, request, *args, **kwargs):
        bicycle = get_object_or_404(Bicycle, pk=self.kwargs['pk'])
        if bicycle.owner != request.user:
            # messages.add_message(self.request, messages.ERROR, "Вы не можете удалить чужое заявление")
            raise PermissionDenied
        messages.add_message(self.request, messages.SUCCESS, "Заявление успешно удалено")
        return super(BicycleDelete, self).dispatch(request, *args, **kwargs)