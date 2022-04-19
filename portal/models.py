from django.db import models
from users.models import Users


class Project(models.Model):
    project_name = models.CharField(max_length=255, blank=True, null=True)
    project_duration = models.CharField(max_length=255, blank=True, null=True)
    project_comments = models.JSONField(blank=True, null=True)
    project_team = models.ManyToManyField(Users)
    project_start_date = models.CharField(max_length=255, blank=True, null=True)
    project_end_date = models.CharField(max_length=255, blank=True, null=True)
    project_progress = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.project_name}"
