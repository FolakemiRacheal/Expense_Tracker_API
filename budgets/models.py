from django.db import models
from category.models import Category
from django.conf import settings

# Create your models here.
class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,null=True,blank=True, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
  

class Meta:
   unique_together = ("user", "category")

