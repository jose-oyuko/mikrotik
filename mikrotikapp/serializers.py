from mikrotikapp.models import PendingPayment, PayedTransaction, Packages
from rest_framework import serializers

class PendingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingPayment
        fields = '__all__'

class PayedTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayedTransaction
        fields = [
            'transaction_id',
            'reference',
            'origination_time',
            'sender_phone_number',
            'amount',
            'till_number',
            'sender_first_name',
            'sender_middle_name',
            'sender_last_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'