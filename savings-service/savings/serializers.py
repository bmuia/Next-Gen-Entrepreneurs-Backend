from rest_framework import serializers
from .models import SavingsAccount

class SavingsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsAccount
        fields = ['id', 'account_holder', 'balance', 'created_at']
        read_only_fields = ['id', 'created_at','account_holder']
    
    def validate_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Balance cannot be negative.")
        return value
    
    
