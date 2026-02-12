from django.db import models
from django.conf import settings

# Create your models here.
class Transaction(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
     amount = models.DecimalField(max_digits=12, decimal_places=2)
     
     TYPE_CHOICES =[
        ("income","Income"),
        ("expense","Expense"),
    ]
     type = models.CharField(max_length=10, choices=TYPE_CHOICES)
     category = models.ForeignKey("category.Category",on_delete=models.SET_NULL,null=True)
     description = models.TextField(blank=True)
     currency = models.CharField(max_length=5, default="NGN")
     transaction_date = models.DateField()
     is_recurring = models.BooleanField(default=False)
     parent_transaction = models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return f"{self.type} - {self.amount}"





# POST   /transactions
# GET    /transactions
# GET    /transactions/:id
# PATCH  /transactions/:id
# DELETE /transactions/:id
