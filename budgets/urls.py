from django.urls import path, include
from .views import BudgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("budgets",BudgetViewSet, basename="budgets")
urlpatterns = [
    path("", include(router.urls)),
]