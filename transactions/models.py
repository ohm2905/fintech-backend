from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10)  # income or expense

    def __str__(self):
        return self.name
    
from django.conf import settings

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    type = models.CharField(max_length=10)  # income or expense
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"
    
