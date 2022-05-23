from statistics import mode
from django.db import models
from users.models import Users
import datetime
from django.db.models import Sum

class Project(models.Model):
    project_name = models.CharField(max_length=255, blank=True, null=True)
    project_duration = models.IntegerField(blank=True, null=True)
    project_comments = models.JSONField(default=list, blank=True, null=True)
    project_team = models.ManyToManyField(Users)
    project_start_date = models.CharField(max_length=255, blank=True, null=True)
    project_end_date = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    project_progress = models.FloatField(blank=True, null=True)
    sentiment = models.FloatField(default=0.0)
    server_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project_name}"
    
    @classmethod
    def create(cls, validated_data):
        project = cls(
            project_name=validated_data.get('project_name'), 
            project_duration=validated_data.get('project_duration'), 
            project_start_date=validated_data.get('project_start_date'), 
            project_end_date=validated_data.get('project_end_date'), 
            description=validated_data.get('description'), 
            project_progress=0, 
        )
        project.save()
        project.project_team.add(validated_data.get('project_team'))
        project.save()
        return project


    def add_comment(self, author, comment, sentiment):
        new_comment = Comment(author=author, project=self, comment=comment, sentiment=sentiment, date=datetime.datetime.now().strftime("%d %B, %Y"))
        new_comment.save()
        comments = Comment.objects.filter(project=self, sentiment__gte=0)
        self.sentiment = round(comments.aggregate(Sum('sentiment')).get('sentiment__sum')/comments.count(), 2)
        self.project_comments = [i.id for i in comments]
        self.save()

    def add_user(self, user):
        self.project_team.add(user)
        self.save()
    
    def update_status(self):
        self.server_status = not self.server_status
        self.save()

        


class Comment(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="comment_author", blank=False, null=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="comment_project", blank=False, null=False)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    date = models.CharField(max_length=20, null=True)
    sentiment = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.author}- {self.project}"

    