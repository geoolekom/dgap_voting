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



