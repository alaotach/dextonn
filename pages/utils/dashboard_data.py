from trade_executor import client
from signal_reader import SignalReader
import os
import importlib


def get_dashboard_data():
        """
        Example function that fetches account data, positions, and orders from trade_executor.
        Adjust as needed for your actual logic.
        """
        current_dir = os.path.dirname(__file__)
        SIGNAL_FILE = os.path.join(current_dir, '..', 'signal.txt')
        signal_reader = SignalReader(SIGNAL_FILE)
        latest_signal = signal_reader.get_latest_signal()
        account_data = {}
        try:
            # Get account (wallet) balance
            balance_response = client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
            balance_info = balance_response['result']['list'][0]
            account_data['balance'] = float(balance_info['totalAvailableBalance'])
            account_data['equity'] = float(balance_info['totalEquity'])
            account_data['available_margin'] = float(balance_info['totalMarginBalance'])
        except Exception as e:
            # print(f"Error fetching wallet balance: {e}")
            pass

        # Get positions
        positions = []
        try:
            position_response = client.get_positions(category='linear', settleCoin='USDT')
            positions_raw = position_response['result']['list']
            # Restructure for your table
            for p in positions_raw:
                positions.append({
                    'symbol': p.get('symbol', ''),
                    'size': p.get('size', 0),
                    'entry_price': p.get('avgPrice', 0),
                    'current_price': p.get('markPrice', 0),
                    'pnl': p.get('unrealisedPnl', 0)
                })
        except Exception as e:
            # print(f"Error fetching positions: {e}")
            pass

        # Get open orders
        orders = []
        try:
            # If needed, specify a symbol, or fetch for all if your API supports it
            orders_response = client.get_open_orders(category='linear', openOnly=0, limit=50, settleCoin='USDT')
            orders_raw = orders_response['result']['list']
            for o in orders_raw:
                orders.append({
                    'symbol': o.get('symbol', ''),
                    'type': o.get('orderType', ''),
                    'side': o.get('side', ''),
                    'price': o.get('price', 0),
                    'amount': o.get('qty', 0),
                    'status': o.get('orderStatus', '')
                })
        except Exception as e:
            # print(f"Error fetching orders: {e}")
            pass

        return account_data, positions, orders