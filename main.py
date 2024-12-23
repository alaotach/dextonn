import sys
import os
import importlib.util
from PyQt5.QtWidgets import QApplication
from auth_window import AuthWindow
from main_window import MainWindow

class TradingApp:
    def __init__(self):
        self.config = self.load_config()
        self.app = QApplication(sys.argv)
        self.auth_window = AuthWindow()
        self.main_window = None
        
        # Connect authentication signal
        self.auth_window.login_success.connect(self.show_main_window)
        
        self.auth_window.show()
        
        # Load configuration

    def load_config(self):
        try:
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.dextton_ai')
            os.makedirs(config_dir, exist_ok=True)
            config_path = os.path.join(config_dir, 'config.py')

            if not os.path.exists(config_path):
                # Create a default config file if it doesn't exist
                with open(config_path, 'w') as f:
                    f.write('API_KEY = ""\n')
                    f.write('API_SECRET = ""\n')
                    f.write('CAPITAL_PERCENTAGE = 0.1\n')
                    f.write('DISCORD_API_KEY = ""\n')
                # print("Default configuration file created.")

            # Import config dynamically
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)

            # print("Configuration loaded successfully!")
            return config
        except Exception as e:
            print(f"No existing config found or error loading: {str(e)}")
            return None

    def show_main_window(self, username):
        self.auth_window.hide()
        self.main_window = MainWindow(username)
        self.main_window.show()
    
    def run(self):
        return self.app.exec_()

if __name__ == '__main__':
    app = TradingApp()
    sys.exit(app.run())