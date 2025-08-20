from django.db import models

# Create your models here.
class Goal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('failed', 'Failed'),
    ]

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    target = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    user_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return self.title
