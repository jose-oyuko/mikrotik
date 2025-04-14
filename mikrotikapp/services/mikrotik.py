import routeros_api
from django.shortcuts import redirect
from django.conf import settings
from loguru import logger
import os

class MikrotikConfigError(Exception):
    """Custom exception for Mikrotik configuration errors"""
    pass

class Miktotik():
    def __init__(self):
        self._validate_config()
        self.mikrotik_ip = settings.MIKROTIK['MIKROTIK_IP']
        self.mikrotik_user = settings.MIKROTIK['MIKROTIK_USER']
        self.mikrotik_pass = settings.MIKROTIK['MIKROTIK_PASS']

    def _validate_config(self):
        """Validate Mikrotik configuration settings"""
        required_settings = ['MIKROTIK_IP', 'MIKROTIK_USER', 'MIKROTIK_PASS']
        
        # Check if MIKROTIK settings exist
        if not hasattr(settings, 'MIKROTIK'):
            raise MikrotikConfigError("MIKROTIK settings not found in Django settings")
            
        # Check for required settings
        missing_settings = [setting for setting in required_settings 
                          if setting not in settings.MIKROTIK or not settings.MIKROTIK[setting]]
        
        if missing_settings:
            raise MikrotikConfigError(f"Missing required Mikrotik settings: {', '.join(missing_settings)}")
            
        logger.debug("Mikrotik configuration validated successfully")

    def get_mt_api(self):
        logger.debug(f"Attempting to connect to Mikrotik router at {self.mikrotik_ip}")
        try:
            api_pool = routeros_api.RouterOsApiPool(
                self.mikrotik_ip,
                username=self.mikrotik_user,
                password=self.mikrotik_pass,
                plaintext_login=True
            )
            api = api_pool.get_api()
            logger.success(f"Successfully connected to Mikrotik router at {self.mikrotik_ip}")
            return api
        except Exception as e:
            logger.error(f"Failed to connect to Mikrotik router at {self.mikrotik_ip}. Error: {str(e)}")
            raise

    def login_user(self, mac, ip):
        logger.info(f"Attempting to login user - MAC: {mac}, IP: {ip}")
        try:
            api = self.get_mt_api()
            api.get_resource('/ip/hotspot/active').call('login', {
                'user': mac,
                'password': mac,
                'mac-address': mac,
                'ip': ip
            })
            logger.success(f"User successfully logged in - MAC: {mac}, IP: {ip}")
            return redirect("https://google.com")
        except Exception as e:
            logger.error(f"Failed to login user - MAC: {mac}, IP: {ip}. Error: {str(e)}")
            raise

    def add_user(self, username, password, time):
        logger.info(f"Attempting to add user - Username: {username}, Time limit: {time}")
        try:
            isUser = self.user_exists(username)
            if isUser:
                logger.info(f"User already exists - Username: {username}")
                return
            
            api = self.get_mt_api()
            api.get_resource('/ip/hotspot/user').call('add', {
                'name': username,
                'password': password,
                'profile': 'default',
                'limit-uptime': time, 
            })
            logger.success(f"User successfully added - Username: {username}, Time limit: {time}")
        except Exception as e:
            logger.error(f"Failed to add user - Username: {username}. Error: {str(e)}")
            raise

    def user_exists(self, username):
        logger.debug(f"Checking if user exists - Username: {username}")
        try:
            api = self.get_mt_api()
            user_resource = api.get_resource('/ip/hotspot/user')
            existing_users = user_resource.get(name=username)
            exists = len(existing_users) > 0
            logger.debug(f"User existence check result - Username: {username}, Exists: {exists}")
            return exists
        except Exception as e:
            logger.error(f"Failed to check user existence - Username: {username}. Error: {str(e)}")
            raise