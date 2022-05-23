from django.contrib import admin
from .models import Project, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'project_name',
        'project_duration',
        'sentiment',
        'project_comments',
        'project_start_date',
        'project_end_date',
        'project_progress',
        'server_status',
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'author',
        'project',
        'sentiment',
        'comment',
        'date',
        
    ]
