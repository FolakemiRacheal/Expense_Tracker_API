from django.urls import path
from .views import (
    MonthlySummaryView,
    CategoryBreakdownView,
    SpendingTrendsView,
    BudgetAlertsView,
    TopMerchantsView,
)

urlpatterns = [
    path('summary/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('category-trends/', CategoryBreakdownView.as_view(), name='category-breakdown'),
    path('trends/', SpendingTrendsView.as_view(), name='spending-trends'),
    path('alerts/', BudgetAlertsView.as_view(), name='budget-alerts'),
    path('merchants/', TopMerchantsView.as_view(), name='top-merchants'),
]