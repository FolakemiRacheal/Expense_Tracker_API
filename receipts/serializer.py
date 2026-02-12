from rest_framework import serializers
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model= Receipt
        fields = (
            "user",
            "image",
            "status",
            "parsed_date",
            "parsed_amount",
            "merchant_name",
            "transaction",
            "uploaded_at"
        )

    read_only_fields = ("status","parsed_date","parsed_amount","uploaded_at")


    def validate_image(self, data):
        user = self.context["request"].user
        if data.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size cannot exceed 5MB.")
                   