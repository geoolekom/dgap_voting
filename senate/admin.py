from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Department, Employee, Category, Issue, Event#, EventDocument


"""class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    fields = ['groups']"""


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'head']
    readonly_fields = ['members']
    # inlines = [UserInline]


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["person", 'department', 'position', 'phone', 'public', 'importance']
    list_editable = ['public', 'importance']
    list_filter = ['department', 'public']
    search_fields = ["person__first_name", "person__last_name"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']


class EventInline(admin.StackedInline):
    model = Event
    can_delete = True
    readonly_fields = ['images_tags']


class IssueAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'author', 'status', 'add_dttm', 'last_event', 'want_to_help',
                    'assigned_dept']
    list_filter = ['category', 'status', 'want_to_help', 'assigned_dept']
    inlines = [EventInline]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Event)
#admin.site.register(EventDocument)


