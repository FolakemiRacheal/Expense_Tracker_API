from rest_framework import serializers
from .models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            "id",
            "user",
            "image",
            "status",
            "parsed_amount",
            "parsed_date",
            "merchant_name",
            "transaction",
            "uploaded_at",
        )
        read_only_fields = ("user", "uploaded_at", "status", "parsed_amount", "parsed_date", "merchant_name")

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Image size cannot exceed 5MB")
        
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("File must be an image")
        
        return value