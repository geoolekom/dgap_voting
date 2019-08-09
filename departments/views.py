from django.views.generic import DetailView

from departments.models import Department, Activist


class DepartmentDetail(DetailView):
    template_name = 'departments/department_detail.html'
    model = Department


class ActivistDetail(DetailView):
    template_name = 'departments/activist_detail.html'
    model = Activist

