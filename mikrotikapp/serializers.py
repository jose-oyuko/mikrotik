from mikrotikapp.models import PendingPayment, PayedTransactions
from rest_framework import serializers

class PendingPaymentSerializer(serializers.ModelSerializer):
    model = PendingPayment
    fields = ['id', 'phoneNumber', 'macAddress', 'ipAddress', 'payed', 'time', 'amount']

class PayedTransactionsSerializer(serializers.ModelSerializer):
    model = PayedTransactions
    fields = ['id', 'phoneNumber', 'timePayed', 'amountPayed', 'package']
