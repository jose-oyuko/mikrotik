import json
import os
from datetime import datetime
from loguru import logger
from django.conf import settings

def save_transaction_to_json(transaction_data):
    """
    Save transaction data to a JSON file.
    Each transaction is appended to the file with a timestamp.
    """
    try:
        # Create transactions directory if it doesn't exist
        transactions_dir = os.path.join(settings.BASE_DIR, 'transactions')
        if not os.path.exists(transactions_dir):
            os.makedirs(transactions_dir)

        # Define the JSON file path
        json_file = os.path.join(transactions_dir, 'transactions.json')

        # Prepare the transaction data with timestamp
        transaction_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': transaction_data
        }

        # Read existing transactions or create new list
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                try:
                    transactions = json.load(f)
                except json.JSONDecodeError:
                    transactions = []
        else:
            transactions = []

        # Append new transaction
        transactions.append(transaction_entry)

        # Write back to file
        with open(json_file, 'w') as f:
            json.dump(transactions, f, indent=2)

        logger.info(f"Transaction saved to JSON file: {transaction_data.get('data', {}).get('id', 'unknown')}")
        return True

    except Exception as e:
        logger.error(f"Error saving transaction to JSON: {str(e)}")
        return False

def get_kopokopo_settings():
    """
    Get Kopokopo API settings from environment variables
    """
    return {
        'client_id': settings.KOPOKOPO['CLIENT_ID'],
        'client_secret': settings.KOPOKOPO['CLIENT_SECRET'],
        'till_number': settings.KOPOKOPO['TILL_NUMBER'],
        'callback_url': settings.KOPOKOPO['CALLBACK_URL'],
    }

def get_network_settings():
    """
    Get network settings from environment variables
    """
    return {
        'default_gateway': settings.NETWORK['DEFAULT_GATEWAY'],
        'dns_servers': settings.NETWORK['DNS_SERVERS'],
    }

def setup_logging():
    """
    Configure logging based on environment variables
    """
    log_level = settings.LOG_LEVEL
    log_file = settings.LOG_FILE

    # Remove default handler
    logger.remove()

    # Add file handler
    logger.add(
        log_file,
        rotation="500 MB",
        retention="10 days",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    # Add console handler
    logger.add(
        lambda msg: print(msg),
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    return logger 