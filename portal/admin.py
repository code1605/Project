from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name',
        'project_duration',
        'project_comments',
        'project_start_date',
        'project_end_date',
        'project_progress'
    ]
