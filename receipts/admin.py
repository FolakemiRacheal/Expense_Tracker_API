from django.contrib import admin
from .models import Receipt

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'merchant_name', 'parsed_amount', 'uploaded_at']
    list_filter = ['status', 'uploaded_at']
    search_fields = ['user__email', 'merchant_name']
    readonly_fields = ['uploaded_at']