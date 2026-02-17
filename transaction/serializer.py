from rest_framework import serializers
from .models import Transaction
from category.models import Category

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "amount",
            "type",
            "category",
            "description",
            "transaction_date",
            "is_recurring",
            "parent_transaction",
            "created_at",
        )
        read_only_fields = ("user", "created_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def validate(self, data):
        category = data.get("category")
        transaction_type = data.get("type")
        
        if category and category.type != transaction_type:
            raise serializers.ValidationError(
                f"Category type '{category.type}' doesn't match transaction type '{transaction_type}'"
            )
        
        return data