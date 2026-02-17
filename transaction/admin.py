from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'amount', 'category', 'transaction_date', 'created_at']
    list_filter = ['type', 'is_recurring', 'transaction_date']
    search_fields = ['user__email', 'description', 'category__name']
    readonly_fields = ['created_at']
    date_hierarchy = 'transaction_date'