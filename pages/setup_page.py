from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSlider, QPushButton,
    QGroupBox, QFormLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from utils.error_handler import show_error, show_info
from styles import STYLES
import os
import importlib
import sys
from trade_executor import reload_config_1
from bot import reload_config_2

class SetupPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_config()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Trading Bot Configuration")
        title.setStyleSheet(STYLES['page_title'])
        main_layout.addWidget(title, alignment=Qt.AlignCenter)

        # API Configuration
        api_group = self.create_api_group()
        main_layout.addWidget(api_group)

        # Trading Parameters
        trading_group = self.create_trading_group()
        main_layout.addWidget(trading_group)

        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.test_api_btn = QPushButton("Test API Connection")
        self.test_api_btn.setStyleSheet(STYLES['secondary_button'])
        self.test_api_btn.clicked.connect(self.test_api_connection)
        buttons_layout.addWidget(self.test_api_btn)

        self.save_btn = QPushButton("Save Configuration")
        self.save_btn.setStyleSheet(STYLES['primary_button'])
        self.save_btn.clicked.connect(self.save_configuration)
        buttons_layout.addWidget(self.save_btn)

        main_layout.addLayout(buttons_layout)
        # self.output_text = QTextEdit()
        # self.output_text.setReadOnly(True)
        # self.output_text.setStyleSheet(STYLES['text_area'])
        # main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)
    
    def load_config(self):
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.dextton_ai')
            config_path = os.path.join(config_dir, 'config.py')

            if not os.path.exists(config_path):
                raise FileNotFoundError("Configuration file not found.")

            # Import config dynamically
            spec = importlib.util.spec_from_file_location("config", config_path)
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)

            # Update UI with loaded values
            self.api_key_input.setText(getattr(config, 'API_KEY', ''))
            self.api_secret_input.setText(getattr(config, 'API_SECRET', ''))
            self.discord_api_input.setText(config.DISCORD_API_KEY)
            cap_percentage = int(getattr(config, 'CAPITAL_PERCENTAGE', 0.1) * 100)
            self.cap_slider.setValue(cap_percentage)
            # self.output_text.append("Configuration loaded successfully!")

    def create_api_group(self):
        group = QGroupBox("API Configuration")
        group.setStyleSheet(STYLES['group_box'])
        layout = QFormLayout()
        layout.setSpacing(15)

        # API Key section
        self.api_key_input = QLineEdit()
        self.api_key_input.setStyleSheet(STYLES['input_field_setup'])
        self.api_key_input.setPlaceholderText("Enter your API key")
        api_key_help = QLabel("1. Get your Bybit API Key from Account Settings → API Management")
        api_key_help.setStyleSheet("color: #7aa2f7; font-size: 12px; padding: 5px 0;")
        
        # API Secret section
        self.api_secret_input = QLineEdit()
        self.api_secret_input.setStyleSheet(STYLES['input_field_setup'])
        self.api_secret_input.setPlaceholderText("Enter your API secret")
        api_secret_help = QLabel("2. Copy your API Secret - it will only be shown once")
        api_secret_help.setStyleSheet("color: #7aa2f7; font-size: 12px; padding: 5px 0;")

        # Discord API section
        self.discord_api_input = QLineEdit()
        self.discord_api_input.setStyleSheet(STYLES['input_field_setup'])
        self.discord_api_input.setPlaceholderText("Enter your Discord API key")
        discord_api_help = QLabel("3. Enter the Discord API key for receiving signals - Get it from Dextton discord bot using <b style='color: yellow'>/key</b> command")
        discord_api_help.setStyleSheet("color: #7aa2f7; font-size: 12px; padding: 5px 0;")

        # Add to layout
        layout.addRow("API Key:", self.api_key_input)
        layout.addRow("", api_key_help)
        layout.addRow("API Secret:", self.api_secret_input)
        layout.addRow("", api_secret_help)
        layout.addRow("Discord API Key:", self.discord_api_input)
        layout.addRow("", discord_api_help)

        group.setLayout(layout)
        return group

    def create_trading_group(self):
        group = QGroupBox("Trading Parameters")
        group.setStyleSheet(STYLES['group_box'])
        layout = QFormLayout()
        layout.setSpacing(15)

        self.cap_slider = QSlider(Qt.Horizontal)
        self.cap_slider.setStyleSheet(STYLES['slider'])
        self.cap_slider.setMinimum(1)
        self.cap_slider.setMaximum(100)
        self.cap_slider.setValue(10)
        self.cap_slider.setTickPosition(QSlider.TicksBelow)
        self.cap_slider.setTickInterval(10)

        self.cap_value_label = QLabel("10%")
        self.cap_value_label.setStyleSheet(STYLES['value_label'])
        self.cap_slider.valueChanged.connect(
            lambda v: self.cap_value_label.setText(f"{v}%"))

        cap_layout = QHBoxLayout()
        cap_layout.addWidget(self.cap_slider)
        cap_layout.addWidget(self.cap_value_label)

        layout.addRow("Capital Percentage:", cap_layout)

        group.setLayout(layout)
        return group

    def save_configuration(self):
        api_key = self.api_key_input.text()
        api_secret = self.api_secret_input.text()
        capital_percentage = self.cap_slider.value() / 100
        reload_config_1()
        reload_config_2()

        try:
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, '.dextton_ai')
            config_path = os.path.join(config_dir, 'config.py')
            # self.output_text.append(f"Saving config to {config_path}")
            
            with open(config_path, 'w') as f:
                f.write(f'API_KEY = "{api_key}"\n')
                f.write(f'API_SECRET = "{api_secret}"\n')
                f.write(f'CAPITAL_PERCENTAGE = {capital_percentage}\n')
                f.write(f'DISCORD_API_KEY = "{self.discord_api_input.text()}"\n')
            
            # self.output_text.append('Config saved successfully!')
            show_info(self, "Success", "Configuration saved successfully! \n Please Restart The Application To Load New Configuration!")
        
        except Exception as e:
            error_msg = f"Error saving config: {str(e)}"
            # self.output_text.append(error_msg)
            show_error(self, "Error", error_msg)

    def test_api_connection(self):
        try:
            from pybit.unified_trading import HTTP
            # Initialize Bybit client
            client = HTTP(testnet=True, api_key=self.api_key_input.text(), api_secret=self.api_secret_input.text())
            
            # Test API connection by fetching account balance
            response = client.get_wallet_balance(accountType="UNIFIED",coin="USDT")
            # print(response)
            
            if response['retCode'] == 0:
                show_info(self, "Success", "API connection successful!")
            else:
                show_error(self, "Error", f"API connection failed: Invalid API KEY")
        except Exception as e:
            show_error(self, "Error", f"API connection failed: {str(e)}")