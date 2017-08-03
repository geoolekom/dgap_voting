from django.contrib import admin
from .models import AidRequest, Category, AidDocument
# Register your models here.

admin.site.register(Category)
admin.site.register(AidRequest)
admin.site.register(AidDocument)
