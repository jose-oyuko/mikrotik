from mikrotikapp.models import PendingPayment, PayedTransaction, Packages
from mikrotikapp.serializers import PayedTransactionSerializer, PendingPaymentSerializer, PackagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist
from loguru import logger
from django.http import HttpResponse
from django.shortcuts import render
from .utils import save_transaction_to_json
from datetime import datetime
import json

class PendingPayment(generics.CreateAPIView):
    queryset = PendingPayment.objects.all()
    serializer_class = PendingPaymentSerializer
    # stk push

class PayedTransactions(generics.CreateAPIView):
    queryset = PayedTransaction.objects.all()
    serializer_class = PayedTransactionSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Convert request body to string and replace 'nil' with 'null'
            if isinstance(request.body, bytes):
                body_str = request.body.decode('utf-8')
            else:
                body_str = str(request.body)
            
            body_str = body_str.replace(': nil', ': null')
            
            # Parse the modified JSON
            try:
                data = json.loads(body_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error after nil replacement: {str(e)}")
                return Response(
                    {'error': 'Invalid JSON format', 'details': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the incoming request data
            logger.debug(f"Received webhook data: {json.dumps(data, indent=2)}")

            # Save the complete transaction data to JSON file
            save_transaction_to_json(data)

            # Extract the required fields from the Kopokopo webhook data
            data = data.get('data', {})
            if not data:
                logger.error("No 'data' field found in webhook payload")
                return Response(
                    {'error': 'Invalid webhook payload: missing data field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            attributes = data.get('attributes', {})
            if not attributes:
                logger.error("No 'attributes' field found in data")
                return Response(
                    {'error': 'Invalid webhook payload: missing attributes field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            event = attributes.get('event', {})
            if not event:
                logger.error("No 'event' field found in attributes")
                return Response(
                    {'error': 'Invalid webhook payload: missing event field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            resource = event.get('resource', {})
            if not resource:
                logger.error("No 'resource' field found in event")
                return Response(
                    {'error': 'Invalid webhook payload: missing resource field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the extracted resource data
            logger.debug(f"Extracted resource data: {json.dumps(resource, indent=2)}")

            try:
                # Parse the origination time
                origination_time = resource.get('origination_time')
                if origination_time:
                    # Remove 'Z' and add timezone if present
                    if origination_time.endswith('Z'):
                        origination_time = origination_time[:-1] + '+00:00'
                    parsed_time = datetime.fromisoformat(origination_time)
                else:
                    parsed_time = datetime.now()
            except ValueError as e:
                logger.error(f"Error parsing origination_time: {str(e)}")
                parsed_time = datetime.now()

            # Prepare the data for the PayedTransaction model
            transaction_data = {
                'transaction_id': data.get('id'),
                'reference': resource.get('reference'),
                'origination_time': parsed_time,
                'sender_phone_number': resource.get('sender_phone_number'),
                'amount': resource.get('amount'),
                'till_number': resource.get('till_number'),
                'sender_first_name': resource.get('sender_first_name'),
                'sender_middle_name': resource.get('sender_middle_name'),
                'sender_last_name': resource.get('sender_last_name'),
            }

            # Log the prepared transaction data
            logger.debug(f"Prepared transaction data: {json.dumps(transaction_data, indent=2, default=str)}")

            # Create the serializer with the extracted data
            serializer = self.get_serializer(data=transaction_data)
            if not serializer.is_valid():
                logger.error(f"Serializer validation errors: {serializer.errors}")
                return Response(
                    {'error': 'Invalid transaction data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.perform_create(serializer)
            logger.info(f"Payment transaction processed successfully: {transaction_data['reference']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing payment transaction: {str(e)}")
            return Response(
                {'error': 'Failed to process payment transaction', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def check_user(self, phone_number):
        pass

class PackegesList(generics.ListCreateAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer

class PackegesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer

def packages(request):
    packages = Packages.objects.all()
    return render(request, 'packages.html', {'packages':packages})