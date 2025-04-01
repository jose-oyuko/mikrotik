from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class PendingPayment(models.Model):
    phoneNumber = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    macAddress = models.CharField(
        max_length=17,
        validators=[RegexValidator(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', 'Enter a valid MAC address.')]
    )
    ipAddress = models.GenericIPAddressField()
    payed = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        indexes = [
            models.Index(fields=['phoneNumber', 'amount']),
        ]

class PayedTransactions(models.Model):
    phoneNumber = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    timePayed = models.DateTimeField(auto_now_add=True)
    amountPayed = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['phoneNumber']),
            models.Index(fields=['transaction_id']),
        ]

class Packages(models.Model):
    price = models.IntegerField()
    period_in_hours = models.IntegerField()

