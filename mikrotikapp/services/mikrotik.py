import routeros_api
from django.shortcuts import redirect
from django.conf import settings

MIKROTIK_IP = settings.MIKROTIK['MIKROTIK_IP']
MIKROTIK_USER = settings.MIKROTIK['MIKROTIK_USER']
MIKROTIK_PASS = settings.MIKROTIK['MIKROTIK_PASS']

class Miktotik():

    def get_mt_api(self):
        api_pool = routeros_api.RouterOsApiPool(
                MIKROTIK_IP, username=MIKROTIK_USER, password=MIKROTIK_PASS, plaintext_login=True
            )
        api = api_pool.get_api()
        return api

    def login_user(self, mac, ip):
        api = self.get_mt_api()
        try:
            api.get_resource('/ip/hotspot/active').call('login', {
                
                'user': mac,
                'password':mac,
                'mac-address': mac,
                'ip':ip
                
            })
            print("uer logged in")
            
            return redirect("https://google.com")
        except Exception as e:
            print("error while adding active is", e)

    def add_user(self, username, password, time):
        isUser = self.user_exists(username)
        if isUser:
            return
        api = self.get_mt_api()
        api.get_resource('/ip/hotspot/user').call('add', {
            'name':username,
            'password':password,
            'profile': 'default',
            'limit-uptime': time, 
        })
        print("user added")

    def user_exists(self, username):
        # checks if a user exists, returns true if
        api = self.get_mt_api()
        user_resource = api.get_resource('/ip/hotspot/user')
        existing_users = user_resource.get(name=username)
        return len(existing_users) > 0