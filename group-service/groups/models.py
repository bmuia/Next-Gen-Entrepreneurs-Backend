from django.db import models
from django.utils import timezone


class Group(models.Model):
    """
    Represents a chat group.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    creator_id = models.PositiveIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Useful counters
    member_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.member_count}/30)"


class GroupMember(models.Model):
    """
    Represents membership of a user in a group.
    """
    ROLE_CHOICES = (
        ("member", "Member"),
        ("admin", "Admin"),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    user_id = models.PositiveIntegerField()  
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")

    joined_at = models.DateTimeField(default=timezone.now)
    left_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("group", "user_id") 

    def __str__(self):
        return f"User {self.user_id} in {self.group.name} ({self.role})"


class GroupEvent(models.Model):
    """
    Audit trail for all group-related events.
    """
    EVENT_CHOICES = (
        ("created", "Group Created"),
        ("deleted", "Group Deleted"),
        ("joined", "Member Joined"),
        ("left", "Member Left"),
        ("promoted", "Member Promoted"),
        ("demoted", "Member Demoted"),
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="events")
    user_id = models.PositiveIntegerField(blank=True, null=True)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    occurred_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - Group {self.group_id} - User {self.user_id}"
