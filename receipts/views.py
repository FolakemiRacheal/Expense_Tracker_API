from django.shortcuts import render
from .models import Receipt
from .serializer import ReceiptSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import ReceiptFilter

class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ReceiptFilter
    

    def get_queryset(self):
        return Receipt.object.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)