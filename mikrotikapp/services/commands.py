from mikrotikapp.serializers import CommandsSerializer
from loguru import logger

class CommandsServices():
    def login(self, mac, ip, time):
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
            serializer = CommandsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                logger.success(f"Successfully created add_user command for username: {username}")
                return serializer.data
            else:
                logger.error(f"Invalid data for add_user command: {serializer.errors}")
                raise ValueError("Invalid data for add_user command")
        except Exception as e:
            logger.error(f"Error creating add_user command: {str(e)}")
            raise

    
