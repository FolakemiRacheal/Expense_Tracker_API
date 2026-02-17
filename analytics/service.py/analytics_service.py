from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from transaction.models import Transaction
from category.models import Category
from budgets.models import Budget

class AnalyticsService:
    def __init__(self, user):
        self.user = user

    def get_monthly_summary(self, year=None, month=None):
        """Get monthly financial summary"""
        if not year:
            year = timezone.now().year
        if not month:
            month = timezone.now().month

        transactions = Transaction.objects.filter(
            user=self.user,
            transaction_date__year=year,
            transaction_date__month=month
        )

        income = transactions.filter(type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        
        expenses = transactions.filter(type='expense').aggregate(
            total=Sum('amount'))['total'] or 0

        return {
            'year': year,
            'month': month,
            'total_income': float(income),
            'total_expenses': float(expenses),
            'net_balance': float(income - expenses),
            'transaction_count': transactions.count()
        }

    def get_category_breakdown(self, period_days=30):
        """Get spending breakdown by category"""
        start_date = timezone.now().date() - timedelta(days=period_days)
        
        breakdown = Transaction.objects.filter(
            user=self.user,
            transaction_date__gte=start_date,
            type='expense'
        ).values(
            'category__name', 'category__id'
        ).annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        ).order_by('-total_amount')

        return list(breakdown)

    def get_spending_trends(self, months=6):
        """Get spending trends over time"""
        trends = []
        current_date = timezone.now().date()
        
        for i in range(months):
            month_start = current_date.replace(day=1) - timedelta(days=i*30)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            monthly_data = Transaction.objects.filter(
                user=self.user,
                transaction_date__range=[month_start, month_end]
            ).aggregate(
                income=Sum('amount', filter=Q(type='income')) or 0,
                expenses=Sum('amount', filter=Q(type='expense')) or 0
            )
            
            trends.append({
                'month': month_start.strftime('%Y-%m'),
                'income': float(monthly_data['income'] or 0),
                'expenses': float(monthly_data['expenses'] or 0),
                'net': float((monthly_data['income'] or 0) - (monthly_data['expenses'] or 0))
            })
        
        return list(reversed(trends))

    def get_budget_alerts(self):
        """Get budget overspending alerts"""
        alerts = []
        current_month = timezone.now().date().replace(day=1)
        
        budgets = Budget.objects.filter(user=self.user)
        
        for budget in budgets:
            spent = Transaction.objects.filter(
                user=self.user,
                category=budget.category,
                type='expense',
                transaction_date__gte=current_month
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            percentage = (spent / budget.limit_amount) * 100 if budget.limit_amount > 0 else 0
            
            if percentage >= 90:
                alerts.append({
                    'category': budget.category.name,
                    'budget_limit': float(budget.limit_amount),
                    'spent': float(spent),
                    'percentage': round(percentage, 2),
                    'status': 'over_budget' if percentage > 100 else 'near_limit'
                })
        
        return alerts

    def get_top_merchants(self, limit=10):
        """Get top merchants by spending"""
        from receipts.models import Receipt
        
        merchants = Receipt.objects.filter(
            user=self.user,
            merchant_name__isnull=False,
            transaction__isnull=False
        ).values('merchant_name').annotate(
            total_spent=Sum('transaction__amount'),
            transaction_count=Count('transaction')
        ).order_by('-total_spent')[:limit]
        
        return list(merchants)