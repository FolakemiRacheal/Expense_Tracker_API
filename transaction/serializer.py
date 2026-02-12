from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "category",
            "type",
            "description",
            "created_at",
            "parent_transaction",
            "currency",
            "transaction_date",
            "is_recurring",

        )
        read_only_fields = ("user", "created_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def validate(self, data):
        category = data.get("category")
        choice_type = data.get("type")
        parent = data.get("parent_transaction")
        user = self.context["request"].user

        if category and category.type != choice_type:
            raise serializers.ValidationError(
                "Category type must match transaction type"
            )

        if parent and parent.user != user:
            raise serializers.ValidationError(
                "Parent transaction must belong to the same user"
            )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
