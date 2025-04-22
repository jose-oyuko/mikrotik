import k2connect
from django.conf import settings
from loguru import logger

CLIENT_SECRET = settings.KOPOKOPO['CLIENT_SECRET']
API_KEY = settings.KOPOKOPO['API_KEY']
CLIENT_ID = settings.KOPOKOPO['CLIENT_ID']
BASE_URL = settings.KOPOKOPO['BASE_URL']
TILL_NUMBER = settings.KOPOKOPO['TILL_NUMBER']
MY_BASE_URL = settings.MY_BASE_URL


class Kopokopo:
    def authorization(self):
        try:
            logger.info("Initializing Kopokopo authorization")
            k2connect.initialize(CLIENT_ID, CLIENT_SECRET, BASE_URL)
            token_service = k2connect.Tokens
            access_token_request = token_service.request_access_token()
            access_token = token_service.get_access_token(access_token_request)
            
            logger.info("Successfully obtained access token")
            return access_token
        except Exception as e:
            logger.error(f"Failed to obtain authorization token: {str(e)}")
            raise
    
    def stk_push(self, amount, phone_number):
        try:
            logger.info(f"Initializing STK push for amount: {amount}, phone: {phone_number}")
            k2connect.initialize(CLIENT_ID, CLIENT_SECRET, BASE_URL)
            stk_service = k2connect.ReceivePayments

            request_body ={
                "access_token": self.authorization(),
                "callback_url": f"{MY_BASE_URL}/api/payed/",
                "payment_channel": "MPESA",
                "phone_number": f"+254{phone_number}",
                "till_number": TILL_NUMBER,
                "amount": str(amount),
                "first_name": "python_first_name",
                "last_name": "python_last_name",
                "email": "john.doe@gmail.com",
            }

            logger.debug(f"STK push request body: {request_body}")
            stk_push_location = stk_service.create_payment_request(request_body)
            logger.info(f"STK push initiated successfully. Location: {stk_push_location}")
            return stk_push_location
        except Exception as e:
            logger.error(f"Failed to initiate STK push: {str(e)}")
            raise


class KopokopoService:
    def __init__(self):
        try:
            self.client_secret = settings.KOPOKOPO['CLIENT_SECRET']
            self.api_key = settings.KOPOKOPO['API_KEY']
            self.client_id = settings.KOPOKOPO['CLIENT_ID']
            self.base_url = settings.KOPOKOPO['BASE_URL']
            self.till_number = settings.KOPOKOPO['TILL_NUMBER']
            self.callback_url = settings.KOPOKOPO['CALLBACK_URL']
            
            if not all([self.client_secret, self.api_key, self.client_id, self.till_number]):
                raise ValueError("Missing required Kopokopo configuration")
            
            # Initialize Kopokopo client
            self.client = k2connect.initialize(
                client_id=self.client_id,
                client_secret=self.client_secret,
                api_key=self.api_key,
                base_url=self.base_url
            )
            
            logger.info("Kopokopo service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Kopokopo service: {str(e)}")
            raise

    def create_payment_request(self, amount, phone_number):
        """
        Create a payment request using Kopokopo's API
        """
        try:
            payment_request = self.client.payment_request(
                till_number=self.till_number,
                amount=amount,
                phone_number=phone_number,
                callback_url=self.callback_url
            )
            return payment_request
        except Exception as e:
            logger.error(f"Failed to create payment request: {str(e)}")
            raise

    def verify_webhook_signature(self, signature, payload):
        """
        Verify the authenticity of a webhook request
        """
        try:
            return self.client.webhook.verify_signature(signature, payload)
        except Exception as e:
            logger.error(f"Failed to verify webhook signature: {str(e)}")
            raise