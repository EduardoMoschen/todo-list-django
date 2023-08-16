from rest_framework import serializers
from base.models import Task


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'complete', 'created']
