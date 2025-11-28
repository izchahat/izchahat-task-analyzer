from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    title = serializers.CharField()
    due_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    estimated_hours = serializers.FloatField(required=False)
    importance = serializers.IntegerField(required=False)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False)

class AnalyzeRequestSerializer(serializers.Serializer):
    tasks = TaskSerializer(many=True)
    weights = serializers.DictField(required=False)
