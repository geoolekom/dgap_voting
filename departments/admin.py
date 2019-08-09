from django.contrib import admin

from departments.models import Department, Position, Activist, Vacancy


class ActivistInline(admin.TabularInline):
    model = Activist
    fields = 'user', 'department', 'position',
    raw_id_fields = 'user',
    extra = 1


class VacancyInline(admin.TabularInline):
    model = Vacancy
    fields = 'position', 'description', 'is_open',


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug',
    search_fields = 'name', 'slug',
    inlines = ActivistInline,


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = 'name',
    search_fields = 'name',


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = 'position', 'department', 'is_open',
    list_filter = 'is_open', 'department',
    search_fields = 'position__name', 'department__name', 'description',


@admin.register(Activist)
class ActivistAdmin(admin.ModelAdmin):
    list_display = 'user', 'department',
    list_filter = 'department',
    search_fields = 'user__last_name', 'user__first_name', 'user__patronymic', 'department__name',

