import datetime
from django.db import models
from django.contrib.auth.models import User

from typing import List

class Security(models.Model):
    ticker = models.CharField(max_length=12, unique=True)
    currency = models.CharField(max_length=3)
    name = models.CharField(max_length=200)

    @classmethod
    def get_by_ticker(cls, ticker: str):
        """
        Returns the security associated with ticker
        """
        return cls.objects.get(ticker=ticker)

    def prices(self, startDate: datetime.date=None, endDate: datetime.date=None):
        """
        Returns all prices of the security
        """
        if startDate is None and endDate is None:
            return self.securityprice_set.all()
        elif startDate is None and endDate is not None:
            return self.securityprice_set.all()\
                    .filter(date__lte=endDate)
        elif startDate is not None and endDate is None:
            return self.securityprice_set.all()\
                    .filter(date__gte=startDate)
        else:
            return self.securityprice_set.all()\
                    .filter(date__gte=startDate)\
                    .filter(date__lte=endDate)


class Investment(models.Model):
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    security = models.OneToOneField(Security, on_delete=models.CASCADE)


class PyfolioUser(User):
    class Meta:
        proxy = True

    @property
    def investments(self):
        return Investment.objects.filter(user=self)

    def invest(self, security: Security, amount: float) -> Investment:
        """
        Creates a new Investment entry into the database for
        the user.
        """
        investment = Investment(amount=amount, security=security,user=self).save()
        return investment



  
class SecurityPrice(models.Model):
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    security = models.ForeignKey(Security,
                                 on_delete=models.CASCADE)

