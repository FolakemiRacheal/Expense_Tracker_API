from django.shortcuts import render
from category.models import Category
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import CategoryFilter
from category.serializer import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner, IsNotDefaultCategory

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotDefaultCategory]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # Prevent deletion if category has transactions
        if instance.transaction_set.exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Cannot delete category with existing transactions")
        
        super().perform_destroy(instance)