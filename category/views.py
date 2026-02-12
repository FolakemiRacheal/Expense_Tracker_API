from django.shortcuts import render
from category.models import Category
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.filters import CategoryFilter
from category.serializer import CategorySerializer
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = CategoryFilter
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



        # filter_backends = [DjanoFilterBackend, filter.SearchFilter, filter.Orderingfilter]
    # search_fields = ['name', 'description']
    # order_fields = ['name','created_at']