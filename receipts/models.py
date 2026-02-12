from django.db import models
from django.conf import settings

# Create your models here.
class Receipt(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='receipts/')
    status = models.CharField(max_length=20, default='pending')
    parsed_amount = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    parsed_date = models.DateField(null=True)
    merchant_name = models.CharField(max_length=100, null=True)
    transaction = models.ForeignKey('transaction.Transaction', on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
