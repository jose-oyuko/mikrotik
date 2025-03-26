from django.db import models

# Create your models here.
class PendingPayment(models.Model):
    phoneNumber = models.IntegerField()
    macAddress = models.CharField(max_length=50)
    ipAddress = models.CharField(max_length=50)
    payed = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()

class PayedTransactions(models.Model):
    phoneNumber = models.IntegerField()
    timePayed = models.DateTimeField(auto_now_add=True)
    amountPayed = models.IntegerField()
    package = models.CharField(max_length=255)
