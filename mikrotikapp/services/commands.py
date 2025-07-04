from mikrotikapp.serializers import CommandsSerializer
from loguru import logger

class CommandsServices():
    def logout_user(self, mac):
        """ 
        takes mac addres as a parameter and creates a logout command for the user.
        """
        try:
            logger.info(f"Attempting to create logout command for MAC: {mac}")
            params = {
                'mac': mac
            }
            data = {
                'comand_type': 'logout_user',
                'params': params
            }
            serializer = CommandsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.success(f"Successfully created logout command for MAC: {mac}")
                return serializer.data
            else:
                logger.error(f"Invalid data for logout command: {serializer.errors}")
                raise ValueError("Invalid data for logout command")
        except Exception as e:
            logger.error(f"Error creating logout command: {str(e)}")
            raise

    def login(self, mac, ip, time):
        """ 
         takes mac address, ip address and time as parameters and creates a login command for the user.
        """
         # Log the parameters being used to create the command
        try:
            logger.info(f"Attempting to create login command for MAC: {mac}, IP: {ip}")
            params = {
                'mac': mac,
                'ip': ip,
                'time': time
            }

            data = {
                'comand_type': 'login_user',
                'params': params
            }
            serializer = CommandsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.success(f"Successfully created login command for MAC: {mac}")
                return serializer.data
            else:
                logger.error(f"Invalid data for login command: {serializer.errors}")
                raise ValueError("Invalid data for login command")
        except Exception as e:
            logger.error(f"Error creating login command: {str(e)}")
            raise

    def add_user(self, username, password, time):
        """ 
         takes username, password and time as parameters and creates an add_user command for the user."""
        try:
            logger.info(f"Attempting to create add_user command for username: {username}")
            params = {
                'username': username,
                'password': password,
                'time': time
            }
            data = {
                'comand_type': 'add_user',
                'params': params
            }
            print(f"Data for add_user command: {data}")
             # Log the data being sent to the serializer
            logger.debug(f"Data sent to CommandsSerializer: {data}")
            serializer = CommandsSerializer(data=data)
            
            logger.debug(f"Serializer is_valid: {serializer.is_valid()}")
            if serializer.is_valid():
                logger.debug(f"Serializer validated data: {serializer.validated_data}")
                serializer.save()
                logger.success(f"Successfully created add_user command for username: {username}")
                return serializer.data
            else:
                logger.error(f"Invalid data for add_user command: {serializer.errors}")
                raise ValueError("Invalid data for add_user command")
        except Exception as e:
            logger.error(f"Error creating add_user command: {str(e)}")
            raise

    
