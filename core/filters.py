import django_filters
from category.models import Category
from transaction.models import Transaction
from budgets.models import Budget
from receipts.models import Receipt
from notifications.models import Notification


class CategoryFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        field_name="type",
        choices=Category.TYPE_CHOICES
    )
    is_default = django_filters.BooleanFilter()
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ["type", "is_default", "name"]


class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="gte"
    )
    max_amount = django_filters.NumberFilter(
        field_name="amount", lookup_expr="lte"
    )
    start_date = django_filters.DateFilter(
        field_name="transaction_date", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(
        field_name="transaction_date", lookup_expr="lte"
    )
    type = django_filters.ChoiceFilter(
        field_name="type",
        choices=Transaction.TYPE_CHOICES
    )
    category = django_filters.NumberFilter(field_name="category_id")
    is_recurring = django_filters.BooleanFilter()
    description = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Transaction
        fields = [
            "type",
            "category",
            "min_amount",
            "max_amount",
            "start_date",
            "end_date",
            "is_recurring",
            "description",
        ]


class BudgetFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    min_limit = django_filters.NumberFilter(
        field_name="limit_amount", lookup_expr="gte"
    )
    max_limit = django_filters.NumberFilter(
        field_name="limit_amount", lookup_expr="lte"
    )

    class Meta:
        model = Budget
        fields = ["category", "min_limit", "max_limit"]


class ReceiptFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    merchant_name = django_filters.CharFilter(
        lookup_expr="icontains"
    )
    start_date = django_filters.DateFilter(
        field_name="uploaded_at", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(
        field_name="uploaded_at", lookup_expr="lte"
    )

    class Meta:
        model = Receipt
        fields = ["status", "merchant_name", "start_date", "end_date"]


class NotificationFilter(django_filters.FilterSet):
    is_read = django_filters.BooleanFilter()
    type = django_filters.CharFilter()
    start_date = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte"
    )
    end_date = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte"
    )

    class Meta:
        model = Notification
        fields = ["is_read", "type", "start_date", "end_date"]
