from django.utils import timezone
from django.db.models import Sum
from mikrotikapp.models import PayedTransaction, PendingPayment
from loguru import logger

class Dashboard():
    def payed_today(self):
        try:
            # Get today's date
            today = timezone.now().date()
            
            # Get all transactions for today
            transactions = PayedTransaction.objects.filter(
                origination_time__date=today
            ).values(
                'origination_time',
                'amount',
                'sender_phone_number',
                'sender_first_name'
            ).order_by('-origination_time')
            
            # Calculate total amount for today
            total_amount = PayedTransaction.objects.filter(
                origination_time__date=today
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            logger.info(f"Retrieved {len(transactions)} transactions for today with total amount: {total_amount}")
            
            return {
                'transactions': list(transactions),
                'total_amount': total_amount
            }
        except Exception as e:
            logger.error(f"Error in payed_today: {str(e)}")
            return {
                'transactions': [],
                'total_amount': 0
            }

    def pending_payment(self):
        try:
            # Get all pending payments
            pending_payments = PendingPayment.objects.filter(
                payed=False
            ).values(
                'phoneNumber',
                'ipAddress',
                'macAddress',
                'time',
                'amount'
            ).order_by('-time')
            
            # Calculate total amount of pending payments
            total_amount = PendingPayment.objects.filter(
                payed=False
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            logger.info(f"Retrieved {len(pending_payments)} pending payments with total amount: {total_amount}")
            
            return {
                'pending_payments': list(pending_payments),
                'total_amount': total_amount
            }
        except Exception as e:
            logger.error(f"Error in pending_payment: {str(e)}")
            return {
                'pending_payments': [],
                'total_amount': 0
            }

    def active_users(self):
        pass

    
    
