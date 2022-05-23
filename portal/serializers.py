# , , , , , 
from rest_framework import serializers
from users.models import Users
import datetime

class ProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(max_length=100, required=True)
    project_start_date = serializers.CharField(max_length=100, required=True)
    project_end_date = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=100, required=True)
    project_team = serializers.ListField(required=True)

    def validate(self, data):
        user = Users.objects.filter(id=data['project_team'][0]).first()
        if user is None:
            raise serializers.ValidationError('User not found')
        data['project_team'] = user
        data['project_start_date'] = datetime.datetime.strptime(data['project_start_date'], '%m/%d/%Y')
        data['project_end_date'] = datetime.datetime.strptime(data['project_end_date'], '%m/%d/%Y')
        data['project_duration'] = data['project_end_date'] - data['project_start_date']
        data['project_duration'] = data['project_duration'].days
        data['project_start_date'] = data['project_end_date'].strftime("%d %B, %Y")
        data['project_end_date'] = data['project_end_date'].strftime("%d %B, %Y")
        return data

class CommentSerializer(serializers.Serializer):
    project_id = serializers.CharField(max_length=1000, required=True)
    comment = serializers.CharField(max_length=100, required=True)
    