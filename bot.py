import time
import os
import sys
def get_base_path():
    # If running as exe, use sys._MEIPASS, otherwise use script directory
    return os.path.dirname(os.path.abspath(__file__))

# Set file paths based on execution context
base_path = get_base_path()
SIGNAL_FILE = os.path.join(base_path, 'signal.txt')
from signal_reader import SignalReader
from trade_executor import execute_trade, close_positions, cancel_all_orders, get_position_info, handle_null_signal
import requests
import importlib

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
        # print(f"Error loading config: {str(e)}")
        sys.exit(1)

def reload_config_2():
    global config, API_KEY, API_SECRET, CAPITAL_PERCENTAGE
    config = load_config()
    if config:
        API_KEY = config.API_KEY
        API_SECRET = config.API_SECRET
        CAPITAL_PERCENTAGE = config.CAPITAL_PERCENTAGE

config = load_config()

def main():
    print("DON'T CLOSE ME! - Close only when you want to stop the trading bot")
    signal_reader = SignalReader(SIGNAL_FILE)
    active_order_id = None
    previous_signal = None
        
    while True:
        apikey = config.DISCORD_API_KEY
        r = requests.get(
                f'http://20.244.46.100:6969/api?apikey={apikey}',
                timeout=10  # Add timeout
            )
        # print(r)
        data = r.json()
        
        # Extract signal text and timestamp
        signal_text = data.get('text', '')
        timestamp = data.get('timestamp', '')
        
        # Format signal
        formatted_signal = f"{signal_text}\nTimestamp {timestamp}"
        
        # Write to signal.txt
        with open('signal.txt', 'w', encoding='utf-8') as f:
            f.write(formatted_signal)

        
        latest_signal = signal_reader.get_latest_signal()
        
        if latest_signal:
            if latest_signal == '0':
                if previous_signal != '0' and previous_signal != None:
                    close_positions(previous_signal['symbol'])
                    cancel_all_orders(previous_signal['symbol'])
                    previous_signal = None
                    active_order_id = None
                    print("Null signal received. Closed all positions.")
            elif latest_signal != previous_signal:
                try:
                    if active_order_id:
                        # print("hello")
                        close_positions(previous_signal['symbol'])
                        cancel_all_orders(previous_signal['symbol'])
                    order_response = execute_trade(latest_signal)
                    active_order_id = order_response['result']['orderId']
                    previous_signal = latest_signal
                except Exception as e:
                    print(f"Error executing trade: {e}")
            else:
                print("Signal has not changed.")
        else:
            print("No signals found.")
        
        if latest_signal and latest_signal != '0':
            position_info = get_position_info(latest_signal['symbol'])
            # print(f"Position info: {position_info}")

        
        
        time.sleep(20)

if __name__ == "__main__":
    main()