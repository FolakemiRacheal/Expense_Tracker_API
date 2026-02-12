from .models import Budget
from .serializer import BudgetSerializer
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Budget.objects.filter(user=self.request.user)
        return Budget.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

