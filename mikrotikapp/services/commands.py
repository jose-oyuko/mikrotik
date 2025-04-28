from mikrotikapp.serializers import CommandsSerializer

class CommandsServices():
    def login(self, mac, ip, time):
        params = {
            'mac': mac,
            'ip': ip,
            'time': time
        }

        data = {
            'command_type': 'login_user',
            'params': params
        }
        serializer = CommandsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValueError("Invalid data for login command")

    def add_user(self, username, password, time):
        params = {
            'username': username,
            'password': password,
            'time': time
        }
        data = {
            'command_type': 'add_user',
            'params': params
        }
        serializer = CommandsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValueError("Invalid data for add_user command")
