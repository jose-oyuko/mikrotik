from mikrotikapp.models import PendingPayment, PayedTransactions, Packages
from rest_framework import serializers

class PendingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingPayment
        fields = ['id', 'phoneNumber', 'macAddress', 'ipAddress', 'payed', 'time', 'amount']
        read_only_fields = ['id', 'time', 'payed']
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

class PayedTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayedTransactions
        fields = ['id', 'phoneNumber', 'timePayed', 'amountPayed', 'package', 'transaction_id']
        read_only_fields = ['id', 'timePayed']
        
    def validate_amountPayed(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value

class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'