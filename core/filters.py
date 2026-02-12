import django_filters
from category.models import Category
from transaction.models import Transaction
from budgets.models import Budget
from receipts.models import Receipt


class CategoryFilter(django_filters.FilterSet):
    type = django_filters.ChoiceFilter(
        field_name="type",
        choices=Category.TYPE_CHOICES
    )
    is_default = django_filters.BooleanFilter()

    class Meta:
        model = Category
        fields = ["type", "is_default"]


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
    type = django_filters.CharFilter(field_name="type")
    category = django_filters.NumberFilter(field_name="category_id")

    class Meta:
        model = Transaction
        fields = [
            "type",
            "category",
            "min_amount",
            "max_amount",
            "start_date",
            "end_date",
        ]


class BudgetFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")

    class Meta:
        model = Budget
        fields = ["category"]

class ReceiptFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    merchant_name = django_filters.CharFilter(
        lookup_expr="icontains"
    )

    class Meta:
        model = Receipt
        fields = ["status", "merchant_name"]
