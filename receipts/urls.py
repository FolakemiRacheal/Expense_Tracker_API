from django.urls import path, include
from .views import ReceiptViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("receipt", ReceiptViewSet, basename="receipt")
urlpatterns = [
    path("", include(router.urls)),
]