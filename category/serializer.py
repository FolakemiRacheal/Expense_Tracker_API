from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "type",
            "description",
            "created_at",
            "is_default",
            "user",
        )
        read_only_fields = ("user", "created_at", "is_default")

    def validate(self, attrs):
        user = self.context["request"].user
        name = attrs.get("name")
        type_ = attrs.get("type")

        if Category.objects.filter(
            user=user,
            name__iexact=name,
            type=type_
        ).exists():
            raise serializers.ValidationError(
                "You already have a category with this name and type."
            )

        return attrs
  

