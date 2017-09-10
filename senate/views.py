from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from .models import Issue

@method_decorator(login_required, name='dispatch')
class IssueDetail(generic.DetailView):
    model = Issue

