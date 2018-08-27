from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'start_date', 'finish_date', 'completed')

class StandardTaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=200)
    start_date = serializers.DateTimeField()
    finish_date = serializers.DateTimeField()
    completed = serializers.BooleanField()

    def create(self, validated_data):
        """
        Create and return a new `Task` instance, given the validated data.
        """
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Task` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.finish_date = validated_data.get('finish_date', instance.finish_date)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance