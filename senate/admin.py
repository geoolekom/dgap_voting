from django.contrib import admin
from .models import Category, Issue, Event, EventDocument

admin.site.register(Category)
admin.site.register(Issue)
admin.site.register(Event)
admin.site.register(EventDocument)


