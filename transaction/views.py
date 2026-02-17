from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializer import TransactionSerializer
from core.filters import TransactionFilter

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    search_fields = ['description', 'category__name']
    ordering_fields = ['transaction_date', 'amount', 'created_at']
    ordering = ['-transaction_date']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Transaction.objects.filter(user=self.request.user).select_related('category')
        return Transaction.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary"""
        queryset = self.get_queryset()
        
        total_income = sum(t.amount for t in queryset.filter(type='income'))
        total_expense = sum(t.amount for t in queryset.filter(type='expense'))
        balance = total_income - total_expense
        
        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'transaction_count': queryset.count()
        })