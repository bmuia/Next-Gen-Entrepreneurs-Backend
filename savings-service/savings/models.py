from django.db import models

# Create your models here.
class SavingsAccount(models.Model):
    account_holder = models.PositiveIntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_holder} - {self.balance}"
    
    class Meta:
        verbose_name = "Savings Account"
        verbose_name_plural = "Savings Accounts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account_holder']),
            models.Index(fields=['-created_at']),
        ]
