import re
# LEVERAGE = 10

class SignalReader:
    def __init__(self, signal_file):
        self.signal_file = signal_file

    def read_signal(self):
        try:
            with open(self.signal_file, 'r', encoding='utf-8') as file:
                signal_text = file.read()
                # print(signal_text)
                if 'NULL' in signal_text:
                    signal = '0'
                else:
                    signal = self.parse_signal(signal_text)
                    # print(signal)
                    if not signal:
                        raise ValueError("Invalid signal format")
            return signal
        except (ValueError, IOError) as e:
            print(f"Error reading signal: {e}")
            return None

    def parse_signal(self, signal_text):
        try:
            symbol_match = re.search(r'(\w+/\w+)', signal_text)
            side_match = re.search(r'(Buy|Sell)', signal_text, re.IGNORECASE)
            entry_price_match = re.search(r'Enter:\s*([\d.]+)', signal_text)
            exit_price_match = re.search(r'Target Profit\s*([\d.]+)', signal_text)
            stop_loss_match = re.search(r'Stop Loss\s*([\d.]+)', signal_text)
            leverage_match = re.search(r'Leverage\s*([\d.]+)', signal_text)
            timestamp_match = re.search(r'Timestamp\s*([\d.]+)', signal_text)

            if not (symbol_match and side_match and entry_price_match and exit_price_match and stop_loss_match):
                return None

            symbol = symbol_match.group(1).replace('/', '')
            side = side_match.group(1).capitalize()
            entry_price = float(entry_price_match.group(1))
            exit_price = float(exit_price_match.group(1))
            stop_loss = float(stop_loss_match.group(1))
            leverage = float(leverage_match.group(1).replace('x', ''))
            timestamp = float(timestamp_match.group(1))

            return {
                'symbol': symbol,
                'side': side,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'stop_loss': stop_loss,
                'leverage': leverage,
                'timestamp': timestamp
            }
        except Exception as e:
            print(f"Error parsing signal: {e}")
            return None

    def get_latest_signal(self):
        return self.read_signal()