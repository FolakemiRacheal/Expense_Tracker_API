from django.urls import path, include
from .views import ReceiptViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("receipts", ReceiptViewSet, basename="receipts")

urlpatterns = [
    path("", include(router.urls)),
]