from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import TransactionFilter
from transaction.serializer import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = TransactionFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

    def get_queryset(self):
        return Transaction.object.filter(user=self.request.user)
    
