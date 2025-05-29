# from .serializers import SessionsSerializers
from mikrotikapp.serializers import SessionsSerializers
from datetime import datetime, timedelta
from django.utils import timezone
from mikrotikapp.models import sessions
from loguru import logger

class SessionsService():
    def add_session(self, mac_address, phone_number, period, package_amount):
        logger.info(f"Attempting to add/update session - MAC: {mac_address}, Phone: {phone_number}, Period: {period} minutes, Amount: {package_amount}")

        # Use timezone.now() to ensure timezone awareness
        current_time = timezone.now()
        end_time = current_time + timedelta(minutes=period)

        # Check if a session with this MAC address already exists
        existing_session = sessions.objects.filter(mac_address=mac_address).first()

        if existing_session:
            # Update the existing session
            logger.info(f"Existing session found for MAC {mac_address}. Updating session.")
            existing_session.package_amount = package_amount
            existing_session.starting_time = current_time
            existing_session.end_time = end_time
            existing_session.phone_number = phone_number # Update phone number as it might change
            existing_session.period = period # Update period
            existing_session.save()
            logger.success(f"Session updated successfully for MAC: {mac_address}, New End Time: {end_time}")
        else:
            # Create a new session if none exists
            logger.info(f"No existing session found for MAC {mac_address}. Creating new session.")
            session_data = {
                "mac_address": mac_address,
                "package_amount": package_amount,
                "starting_time": current_time, # Explicitly set starting_time for new session
                "end_time": end_time,
                "phone_number": phone_number,
                "period": period
            }

            logger.debug(f"New session data prepared: {session_data}")

            serializer = SessionsSerializers(data=session_data)
            if serializer.is_valid():
                serializer.save()
                logger.success(f"New session created successfully - MAC: {mac_address}, End Time: {end_time}")
            else:
                logger.error(f"Failed to create new session - MAC: {mac_address}, Errors: {serializer.errors}")

    def check_session(self, mac_address):
        try:
            logger.info(f"Checking session status for MAC: {mac_address}")
            
            # Get session by mac_address
            session = sessions.objects.filter(mac_address=mac_address).first()
            
            if not session:
                logger.info(f"No active session found for MAC: {mac_address}")
                return False
                
            # Use timezone.now() instead of datetime.now() to ensure timezone awareness
            current_time = timezone.now()
            
            # Check if session has expired
            if current_time > session.end_time:
                logger.info(f"Session expired for MAC: {mac_address}, End Time: {session.end_time}")
                # Delete expired session
                session.delete()
                return False
                
            # Calculate time remaining
            time_remaining = session.end_time - current_time
            total_seconds = time_remaining.total_seconds()
            
            # Calculate days, hours, and minutes
            days = int(total_seconds // 86400)
            hours = int((total_seconds % 86400) // 3600)
            minutes = int((total_seconds % 3600) // 60)
            
            # Format time remaining string
            time_str = ""
            if days > 0:
                time_str += f"{days}d"
            if hours > 0 or days > 0:
                time_str += f"{hours}h"
            time_str += f"{minutes}m"
            
            logger.info(f"Active session found for MAC: {mac_address}, Time remaining: {time_str}")
            
            return {
                "mac_address": session.mac_address,
                "time_remaining": time_str
            }
            
        except Exception as e:
            logger.error(f"Error checking session for MAC: {mac_address}, Error: {str(e)}")
            return False
