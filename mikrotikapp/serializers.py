from mikrotikapp.models import Tickets, PendingPayment, PayedTransaction, Packages, sessions, Commands
from rest_framework import serializers
import re

class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = '__all__'


class CommandsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Commands
        fields = ['id', 'data', 'executed', 'created_at']

    def get_data(self, obj):
        return {
            'type': obj.comand_type,
            'params': obj.params
        }

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
        fields = ['id', 'period_in_minutes', 'price']

    def validate(self, data):
        # Ensure period_in_minutes is provided
        if not data.get('period_in_minutes'):
            raise serializers.ValidationError("period_in_minutes must be provided")
        return data

    def to_representation(self, instance):
        """Convert the instance to a representation"""
        ret = super().to_representation(instance)
        # Add a human-readable period display
        ret['period_display'] = str(instance)
        return ret