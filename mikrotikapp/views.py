from mikrotikapp.models import PendingPayment, PayedTransactions
from mikrotikapp.serializers import PayedTransactionsSerializer, PendingPaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PendingPayment(APIView):
    def get(self, request, format=None):
        records=PendingPayment.objects.all()
        serializer=PendingPaymentSerializer(records, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PendingPaymentSerializer(data=request.data)
        if serializer.is_valid():
            phoneNumber = serializer.data.get("phoneNumber")
            amount = serializer.data.get("amount")
            serializer.save()
            self.stkPush(phoneNumber, amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def stkPush(self, phoneNumber, amount):
        pass

class PayedTransactions(APIView):
    # this will be the callback from kopokopo api
    def post(self, request, format=None):
        serializer = PayedTransactionsSerializer(data=request.data)
        if serializer.is_valid():
            phoneNumber = serializer.validated_data['phoneNumber']
            amount = serializer.validated_data["amount"]
            serializer.save()
            unpaidRecord = PendingPayment.objects.filter(phoneNumber=phoneNumber, amount=amount).first()
            if unpaidRecord:
                ipAddress = unpaidRecord.ipAddress
                macAdress = unpaidRecord.macAddress
                # autologin the user
                self.autologin(phoneNumber, ipAddress, macAdress)
                # delete the record after processing it
                unpaidRecord.delete()
                

    def autologin(self, phoneNumber, ipAddress, macAdress):
        pass
