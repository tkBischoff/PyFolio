from django.db import models

class Security(models.Model):
    ticker = models.CharField(max_length=12, unique=True)
    currency = models.CharField(max_length=3)
    name = models.CharField(max_length=200)

class SecurityPrice(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    security = models.ForeignKey(Security,
                                 on_delete=models.CASCADE)
