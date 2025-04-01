from mikrotikapp.models import PendingPayment, PayedTransactions, Packages
from mikrotikapp.serializers import PayedTransactionsSerializer, PendingPaymentSerializer, PackagesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist
from loguru import logger
from django.http import HttpResponse
from django.shortcuts import render

class PendingPayment(APIView):
    def get(self, request, format=None):
        try:
            records = PendingPayment.objects.all()
            serializer = PendingPaymentSerializer(records, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching pending payments: {str(e)}")
            return Response(
                {"error": "Failed to fetch pending payments"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request, format=None):
        try:
            serializer = PendingPaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"New pending payment created: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid payment data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error processing payment request: {str(e)}")
            return Response(
                {"error": "Failed to process payment request"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PayedTransactions(APIView):
    def post(self, request, format=None):
        try:
            serializer = PayedTransactionsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"New paid transaction recorded: {serializer.data}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid transaction data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error processing payment callback: {str(e)}")
            return Response(
                {"error": "Failed to process payment callback"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class PackegesList(generics.ListCreateAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer

class PackegesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer

def packages(request):
    packages = Packages.objects.all()
    return render(request, 'packages.html', {'packages':packages})