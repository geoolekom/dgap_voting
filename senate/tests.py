from django.test import TestCase
from django.db.models import QuerySet
from django import forms
from .forms import CascadeWidget, IssueCreateForm
from .models import Category, Department
import pytest
# Create your tests here.
'''class FormTestCase(TestCase):
    def test_default_cache(self):
        from django_select2.cache import cache
        cache.set('key', 'value')
        print(cache.get('key'))
        assert cache.get('key') == 'value'''''


class WidgetTestCase(TestCase):
    def setUp(self):
        for i in range(10):
            Category.objects.create(parent=None, name='parent%i'.format(i))
    def test_get_queryset(self):
        widget = CascadeWidget()
        #with pytest.raises(NotImplementedError):
        #    widget.get_queryset()
        widget.model = Category
        assert isinstance(widget.get_queryset(), QuerySet)
        widget.model = None
        widget.queryset = Category.objects.all()
        assert isinstance(widget.get_queryset(), QuerySet)

    def test_form(self):
        form = IssueCreateForm()
