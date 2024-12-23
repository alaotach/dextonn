from pybit.unified_trading import HTTP
import importlib
import os
import sys


class APIClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance
    
    def load_config():
        try:
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.dextton_ai')
            config_path = os.path.join(config_dir, 'config.py')

            if not os.path.exists(config_path):
                raise FileNotFoundError("Configuration file not found.")

            # Import config dynamically
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)

            return config
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            sys.exit(1)

    config = load_config()
    
    def initialize(self, api_key, api_secret):
        try:
            self.client = HTTP(
                testnet=True,
                api_key=api_key,
                api_secret=api_secret
            )
            return True
        except Exception as e:
            # print(f"API initialization error: {str(e)}")
            return False
    
    def get_balance(self):
        try:
            response = self.client.get_wallet_balance(
                accountType="UNIFIED",
                coin="USDT"
            )
            return response['result']['list'][0]['totalAvailableBalance']
        except Exception as e:
            # print(f"Balance fetch error: {str(e)}")
            return 0.0