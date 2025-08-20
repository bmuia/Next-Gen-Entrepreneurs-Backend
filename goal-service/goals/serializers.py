from .models import Goal
from rest_framework import serializers

class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for the Goal model.
    """
    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'target', 'status', 'user_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'user_id', ]