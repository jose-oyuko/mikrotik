import k2connect
from django.conf import settings
from loguru import logger

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

    def create_payment_request(self, amount, phone_number, description):
        """
        Create a payment request using Kopokopo's API
        """
        try:
            payment_request = self.client.payment_request(
                till_number=self.till_number,
                amount=amount,
                phone_number=phone_number,
                description=description,
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