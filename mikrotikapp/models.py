from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from loguru import logger
from .fields import LastNineDigitsPhoneField

# Create your models here.
class Tickets(models.Model):
    ticketUsername = models.CharField(max_length=100, unique=True)
    ticketPassword = models.CharField(max_length=100, unique=True)
    ticketPeriod = models.IntegerField()
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    


class PendingPayment(models.Model):
    phoneNumber = LastNineDigitsPhoneField(max_length=9)
    macAddress = models.CharField(max_length=17)
    ipAddress = models.GenericIPAddressField()
    payed = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    
    class Meta:
        indexes = [
            models.Index(fields=['phoneNumber', 'amount']),
        ]

    def __str__(self):
        return f"{self.phoneNumber} - Ksh {self.amount}"

class PayedTransaction(models.Model):
    transaction_id = models.CharField(max_length=36, unique=True)  # Kopokopo ID
    reference = models.CharField(max_length=20)  # Kopokopo reference
    origination_time = models.DateTimeField()
    sender_phone_number = LastNineDigitsPhoneField(max_length=9)
    amount = models.IntegerField()
    till_number = models.CharField(max_length=10)
    sender_first_name = models.CharField(max_length=100, null=True, blank=True)
    sender_middle_name = models.CharField(max_length=100, null=True, blank=True)
    sender_last_name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.sender_phone_number} - Ksh {self.amount}"

    class Meta:
        ordering = ['-origination_time']

class Packages(models.Model):
    period_in_minutes = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        minutes = self.period_in_minutes
        if minutes % 60 == 0:  # If minutes is a multiple of 60
            return f"{minutes // 60} hours"
        else:
            return f"{minutes} minutes"

class sessions(models.Model):
    mac_address = models.CharField(max_length=17, unique=True)
    package_amount = models.IntegerField()
    starting_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=False, blank=False)
    phone_number = LastNineDigitsPhoneField(max_length=9)
    period = models.CharField(max_length=15)
    mpesa_code = models.CharField(max_length=20, null=True, blank=True, unique=True)


class Commands(models.Model):
    COMMAND_TYPES = [
        ('add_user', 'Add User'),
        ('login_user', 'Login User'),
        ('remove_user', 'Remove User'),
        ('update_user', 'Update User'),
        ('logout_user', 'Logout User'),
    ]
    comand_type = models.CharField(max_length=50, choices=COMMAND_TYPES)
    params = models.JSONField()
    executed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
