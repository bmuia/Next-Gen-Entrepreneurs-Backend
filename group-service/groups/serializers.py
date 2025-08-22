from rest_framework import serializers
from .models import Group, GroupMember, GroupEvent


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'creator_id', 'created_at', 'member_count']
        read_only_fields = ['id', 'creator_id', 'created_at', 'member_count']


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'user_id', 'role', 'joined_at', 'left_at']
        read_only_fields = ['id', 'joined_at', 'group', 'role', 'left_at','user_id']



class GroupEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupEvent
        fields = ['id', 'group', 'user_id', 'event_type', 'occurred_at']
        read_only_fields = ['id', 'group', 'user_id', 'occurred_at']

class GroupListSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(source='group_members', many=True, read_only=True)
    events = GroupEventSerializer(source='group_events', many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'creator_id', 'created_at', 'member_count', 'members', 'events']

