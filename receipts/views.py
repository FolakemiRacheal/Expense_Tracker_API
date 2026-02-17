from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Receipt
from .serializer import ReceiptSerializer
from core.filters import ReceiptFilter

class ReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReceiptFilter

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Receipt.objects.filter(user=self.request.user)
        return Receipt.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Trigger OCR processing for receipt"""
        receipt = self.get_object()
        
        if receipt.status != 'pending':
            return Response(
                {'error': 'Receipt is already processed or processing'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update status to processing
        receipt.status = 'processing'
        receipt.save()
        
        # TODO: Add Celery task for OCR processing
        # process_receipt_ocr.delay(receipt.id)
        
        return Response({'message': 'Receipt processing started'})

    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """Retry failed OCR processing"""
        receipt = self.get_object()
        
        if receipt.status != 'failed':
            return Response(
                {'error': 'Can only retry failed receipts'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        receipt.status = 'pending'
        receipt.save()
        
        return Response({'message': 'Receipt queued for retry'})