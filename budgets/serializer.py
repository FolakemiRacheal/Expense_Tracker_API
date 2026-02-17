from rest_framework import serializers
from .models import Budget

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = (
            "id",
            "user",
            "category",
            "limit_amount",
        )
        read_only_fields = ("user",)
        
    def validate_limit_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

    def validate(self, data):
        user = self.context["request"].user
        category = data.get("category")

        existing_budgets = Budget.objects.filter(
            user=user,
            category=category,
        ).exclude(pk=self.instance.pk if self.instance else None)

        if existing_budgets.exists():
            raise serializers.ValidationError(
                "A budget already exists for this category."
            )

        return data
