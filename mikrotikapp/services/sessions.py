# from .serializers import SessionsSerializers
from mikrotikapp.serializers import SessionsSerializers
from datetime import datetime, timedelta
from mikrotikapp.models import sessions

class Sessions():
    def add_session(self, mac_address, phone_number, period, package_amount):
        # Calculate end time by adding period (in hours) to current time
        end_time = datetime.now() + timedelta(hours=period)
        
        session_data = {
            "mac_address": mac_address,
            "package_amount": package_amount,
            "end_time": end_time,
            "phone_number": phone_number,
            "period": period
        }
        serializer = SessionsSerializers(data=session_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"failed with errors {serializer.errors}")

    def check_session(self, mac_address):
        try:
            # Get session by mac_address
            session = sessions.objects.filter(mac_address=mac_address).first()
            
            if not session:
                return False
                
            # Check if session has expired
            if datetime.now() > session.end_time:
                # Delete expired session
                session.delete()
                return False
                
            # Calculate time remaining
            time_remaining = session.end_time - datetime.now()
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
            
            return {
                "mac_address": session.mac_address,
                "time_remaining": time_str
            }
            
        except Exception as e:
            print(f"Error checking session: {str(e)}")
            return False
