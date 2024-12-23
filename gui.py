import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QSlider, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer, QProcess
from PyQt5.QtGui import QPixmap, QFont
from pybit.unified_trading import HTTP
import config as config
import json

class ConfigGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.client = HTTP(testnet=True, api_key=config.API_KEY, api_secret=config.API_SECRET)

        # Set up a timer to fetch data periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start(60000)  # Fetch data every 60 seconds

        # Set up QProcess for running the bot
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def initUI(self):
        self.setWindowTitle('Dextton Bot Configuration')
        self.setStyleSheet("background-color: #1e1e2f; color: #ffffff;")

        # Logo
        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('path/to/logo.png')  # Replace with the path to your logo file
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setFixedSize(60, 60)

        # Heading
        self.heading_label = QLabel('DEXTONN BOT', self)
        self.heading_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.heading_label.setStyleSheet("color: #00d1b2;")

        # Header Layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(self.heading_label)
        header_layout.addStretch()

        # API Key
        self.api_key_label = QLabel('API Key:', self)
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setText(config.API_KEY)
        self.api_key_input.setStyleSheet("background-color: #29293d; border: 1px solid #00d1b2; color: #ffffff;")

        # API Secret
        self.api_secret_label = QLabel('API Secret:', self)
        self.api_secret_input = QLineEdit(self)
        self.api_secret_input.setText(config.API_SECRET)
        self.api_secret_input.setStyleSheet("background-color: #29293d; border: 1px solid #00d1b2; color: #ffffff;")

        # Capital Percentage
        self.capital_percentage_label = QLabel('Capital Percentage:', self)
        self.capital_percentage_slider = QSlider(Qt.Horizontal, self)
        self.capital_percentage_slider.setMinimum(0)
        self.capital_percentage_slider.setMaximum(100)
        self.capital_percentage_slider.setValue(int(config.CAPITAL_PERCENTAGE * 100))
        self.capital_percentage_slider.setTickPosition(QSlider.TicksBelow)
        self.capital_percentage_slider.setTickInterval(10)
        self.capital_percentage_slider.setStyleSheet("QSlider::groove:horizontal { height: 8px; background: #29293d; } QSlider::handle:horizontal { background: #00d1b2; width: 18px; }")

        self.capital_percentage_value = QLabel(f'{config.CAPITAL_PERCENTAGE:.2f}', self)
        self.capital_percentage_value.setStyleSheet("color: #00d1b2;")

        self.capital_percentage_slider.valueChanged.connect(self.update_slider_value)

        # Save Button
        self.save_button = QPushButton('Save', self)
        self.save_button.setStyleSheet("background-color: #00d1b2; color: #ffffff; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_config)

        # Run Bot Button
        self.run_bot_button = QPushButton('Run Bot', self)
        self.run_bot_button.setStyleSheet("background-color: #007acc; color: #ffffff; border-radius: 5px;")
        self.run_bot_button.clicked.connect(self.run_bot)

        # Account Balance Text Area
        self.account_balance_text = QTextEdit(self)
        self.account_balance_text.setReadOnly(True)
        self.account_balance_text.setFixedHeight(80)
        self.account_balance_text.setStyleSheet("background-color: #29293d; color: #ffffff; border: 1px solid #00d1b2;")

        # Position Data Text Area
        self.position_data_text = QTextEdit(self)
        self.position_data_text.setReadOnly(True)
        self.position_data_text.setStyleSheet("background-color: #29293d; color: #ffffff; border: 1px solid #00d1b2;")

        # Output Text Area
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #29293d; color: #ffffff; border: 1px solid #00d1b2;")

        # Layout for configuration settings
        config_layout = QVBoxLayout()
        config_layout.addLayout(header_layout)
        config_layout.addWidget(self.api_key_label)
        config_layout.addWidget(self.api_key_input)
        config_layout.addWidget(self.api_secret_label)
        config_layout.addWidget(self.api_secret_input)
        config_layout.addWidget(self.capital_percentage_label)
        config_layout.addWidget(self.capital_percentage_slider)
        config_layout.addWidget(self.capital_percentage_value)
        config_layout.addWidget(self.save_button)
        config_layout.addWidget(self.run_bot_button)

        # Layout for account balance and position data
        data_layout = QVBoxLayout()
        data_layout.addWidget(QLabel('Account Balance:', self))
        data_layout.addWidget(self.account_balance_text)
        data_layout.addWidget(QLabel('Position Data:', self))
        data_layout.addWidget(self.position_data_text)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(data_layout)
        main_layout.addLayout(config_layout)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

    def update_slider_value(self):
        value = self.capital_percentage_slider.value() / 100
        self.capital_percentage_value.setText(f'{value:.2f}')

    def save_config(self):
        api_key = self.api_key_input.text()
        api_secret = self.api_secret_input.text()
        capital_percentage = self.capital_percentage_slider.value() / 100

        try:
            config_path = './config.py'
            with open(config_path, 'w') as f:
                f.write(f'API_KEY = "{api_key}"')
                f.write(f'API_SECRET = "{api_secret}"')
                f.write(f'CAPITAL_PERCENTAGE = {capital_percentage}')
            self.output_text.append('Config saved!')
        except Exception as e:
            self.output_text.append(f"Error saving config: {e}")

    def run_bot(self):
        self.output_text.append('Running bot...')
        self.process.start('cmd', ['/c', 'start', 'cmd', '/k', 'python', 'c:/crypto/trading-bot/src/bot.py'])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode('utf8')
        self.output_text.append(stdout)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode('utf8')
        self.output_text.append(stderr)

    def process_finished(self):
        self.output_text.append('Bot process finished.')

    def fetch_data(self):
        try:
            self.account_balance_text.clear()
            self.position_data_text.clear()
            self.output_text.clear()

            # Fetch signals
            from signal_reader import SignalReader
            signal_reader = SignalReader('C:/crypto/trading-bot/src/signal.txt')
            signal = signal_reader.get_latest_signal()
            symbol = signal['symbol']

            # Fetch account balance
            balance_response = self.client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            balance = balance_response['result']['list'][0]['totalAvailableBalance']
            self.account_balance_text.append(f"{balance} USDT")

            # Fetch current positions
            positions_response = self.client.get_positions(category='linear', symbol=symbol)
            positions = positions_response['result']['list']
            if not positions:
                self.position_data_text.append(f"No positions for {symbol} right now.")
            else:
                for position in positions:
                    entry_price = position['entryPrice']
                    size = position['size']
                    unrealized_pnl = position['unrealizedPnl']
                    self.position_data_text.append(
                        f"Symbol: {symbol}\nEntry Price: {entry_price}\nSize: {size}\nUnrealized PnL: {unrealized_pnl}\n"
                    )
        except Exception as e:
            self.output_text.append(f"Error fetching data: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ConfigGUI()
    ex.resize(1200, 800)  # Adjust the size as needed
    ex.show()
    sys.exit(app.exec_())
