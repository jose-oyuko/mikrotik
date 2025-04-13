from mikrotikapp.models import PendingPayment, PayedTransaction, Packages, sessions
from rest_framework import serializers
import re

class SessionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = sessions
        fields = '__all__'

class PendingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingPayment
        fields = '__all__'

    def validate_phoneNumber(self, value):
        if value:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', value)
            if len(digits) < 9:
                raise serializers.ValidationError('Phone number must have at least 9 digits')
            # Return the original value, our custom field will handle the processing
            return value
        return value

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

    def validate_sender_phone_number(self, value):
        if value:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', value)
            if len(digits) < 9:
                raise serializers.ValidationError('Phone number must have at least 9 digits')
            # Return the original value, our custom field will handle the processing
            return value
        return value

class PackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'