from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    buy_price = models.FloatField()

    def __str__(self):
        return f"{self.stock_name} - {self.user}"