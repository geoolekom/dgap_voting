from django.shortcuts import render
from django.views import generic
from .models import QA

class Faq(generic.ListView):
    model = QA
    template_name = 'faq/faq.html'

    def get_queryset(self):
        return [(item, QA.objects.filter(audience=item[0]).order_by('id'))
                for item in QA.AUDIENCE_CHOICES]
