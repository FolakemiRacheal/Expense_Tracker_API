from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Notification
        fields = (
        "user",
        "title",
        "type",
        "message",
        "is_read",
        "created_at",
    )
    read_only = ("user","is_read", "created_at")    