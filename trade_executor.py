from pybit.unified_trading import HTTP
import os
import importlib
import sys
def load_config():
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

def reload_config_1():
    global config, API_KEY, API_SECRET, CAPITAL_PERCENTAGE
    config = load_config()
    if config:
        API_KEY = config.API_KEY
        API_SECRET = config.API_SECRET
        CAPITAL_PERCENTAGE = config.CAPITAL_PERCENTAGE
        global client 
        client = HTTP(testnet=True, api_key=API_KEY, api_secret=API_SECRET)
        # print(client)
        # print(API_KEY)

config = load_config()
if config:
    API_KEY = config.API_KEY
    API_SECRET = config.API_SECRET
    CAPITAL_PERCENTAGE = config.CAPITAL_PERCENTAGE
else:
    API_KEY = ""
    API_SECRET = ""
    CAPITAL_PERCENTAGE = 0.1

client = HTTP(testnet=True, api_key=API_KEY, api_secret=API_SECRET)
# from utils import log_message
import json
import time
import math
from decimal import Decimal, ROUND_DOWN



def set_leverage(symbol, leverage):
    response = client.set_leverage(
        category='linear',
        symbol=symbol,
        buyLeverage=str(leverage),
        sellLeverage=str(leverage)
    )
    # log_message(f"Set leverage response: {response}")
    if response['retCode'] != 0:
        raise Exception(f"Error setting leverage: {response['retMsg']}")

def place_order(symbol, side, qty, order_type="Limit", price=None, take_profit=None, stop_loss=None):
    # Fetch instrument info to get qtyStep
    instrument_info_response = client.get_instruments_info(category='linear', symbol=symbol)
    # print(instrument_info_response)
    instrument_info = instrument_info_response['result']['list'][0]
    # qty_step = float()

    # Round off the quantity according to qtyStep
    qty_step = Decimal(instrument_info['lotSizeFilter']['qtyStep'])
    print(qty_step)

    # Round off the quantity according to qtyStep
    rounded_qty = round_qty(Decimal(qty), qty_step)

    order_params = {
        "category": "linear",
        "symbol": symbol,
        "side": side,
        "orderType": order_type,
        "qty": str(rounded_qty),  # Ensure qty is a string
        "timeInForce": "GTC",
        "reduceOnly": False,
        "closeOnTrigger": False
    }
    if price:
        order_params["price"] = str(price)  # Ensure price is a string
    if take_profit:
        order_params["takeProfit"] = str(take_profit)  # Ensure take profit is a string
    if stop_loss:
        order_params["stopLoss"] = str(stop_loss)  # Ensure stop loss is a string

    response = client.place_order(**order_params)
    # log_message(f"Place order response: {response}")
    return response

def set_stop_loss(symbol, side, qty, stop_loss_price):
    response = place_order(
        symbol=symbol,
        side='Sell' if side == 'Buy' else 'Buy',
        qty=qty,
        order_type='Market',  # Use Market order type for stop loss
        trigger_price=stop_loss_price  # Set trigger price
    )
    # log_message(f"Set stop loss response: {response}")
    return response

def cancel_order(symbol, order_id=None, order_link_id=None):
    try:
        response = client.cancel_order(
            category='linear',
            symbol=symbol,
            orderId=order_id,
            orderLinkId=order_link_id
        )
        # log_message(f"Cancel order response: {response}")
        return response
    except Exception as e:
        # if "order not exists or too late to cancel" in str(e):
        #     # log_message(f"Order not exists or too late to cancel: {e}")
        # else:
        #     # log_message(f"Error canceling order: {e}")
        raise

def cancel_all_orders(symbol):
    try:
        response = client.cancel_all_orders(
            category='linear',
            symbol=symbol
        )
        # log_message(f"Cancel all orders response: {response}")
        return response
    except Exception as e:
        # log_message(f"Error canceling all orders: {e}")
        raise

def close_positions(symbol):
    while True:
        response = client.get_positions(category='linear', symbol=symbol)
        position = response["result"]['list'][0]
        # print(response)
        # print(symbol)
        # print(position['symbol'])
        # print(position['size'])
        
        if float(position["size"]) > 0 and position["symbol"] == symbol:
            side = 'Sell' if position["side"] == 'Buy' else 'Buy'
            order_params = {
                "category": "linear",
                "symbol": position["symbol"],
                "side": side,
                "orderType": "Market",
                "qty": position["size"],  # Ensure qty is a string
                "timeInForce": "GTC",
                "reduceOnly": True,
                "closeOnTrigger": False
            }
            response = client.place_order(**order_params)
            # print(response)
            time.sleep(1)  # Delay before checking again
        else:
            print(f"Position for {symbol} closed successfully.")
            break

def get_open_orders(symbol):
    try:
        response = client.get_open_orders(
            category='linear',
            symbol=symbol,
            openOnly=0,
            limit=50
        )
        # log_message(f"Get open orders response: {response}")
        return response
    except Exception as e:
        # log_message(f"Error getting open orders: {e}")
        raise

def get_position_info(symbol):
    try:
        response = client.get_positions(
            category='linear',
            symbol=symbol
        )
        # log_message(f"Get position info response: {response}")
        return response
    except Exception as e:
        # log_message(f"Error getting position info: {e}")
        raise

def monitor_market_price(symbol, exit_price, order_id):
    while True:
        try:
            response = client.latest_information_for_symbol(symbol=symbol)
            market_price = float(response['result'][0]['markPrice'])
            # log_message(f"Market price for {symbol}: {market_price}")

            if market_price >= exit_price:
                # log_message(f"Exit price {exit_price} achieved for {symbol}. Closing position.")
                close_positions(symbol)
                break

            time.sleep(10)  # Wait for 10 seconds before checking the price again
        except Exception as e:
            # log_message(f"Error monitoring market price: {e}")
            break

def execute_trade(signal):
    try:
        symbol = signal['symbol']
        side = signal['side']
        entry_price = signal['entry_price']
        exit_price = signal['exit_price']
        stop_loss_price = signal['stop_loss']
        leverage = signal['leverage']
        timestamp = signal['timestamp']
        try:
            set_leverage(symbol, leverage)
        except:
            pass
        current_time = time.time()
        signal_age = current_time - timestamp
        if signal_age > 300:  # 5 minutes = 300 seconds
            print(f"Signal too old. Age: {signal_age} seconds")
            return None

        # print(leverage)

        # log_message(f"Executing trade with signal: {signal}")

        # Fetch market price
        mark = client.get_tickers(
            category="linear",
            symbol=symbol,
        )

        # Fetch account balance
        acc_bal = client.get_wallet_balance(
            accountType="UNIFIED",
            coin="USDT",
        )
        acc_bal = float(acc_bal['result']['list'][0]['totalAvailableBalance'])
        # print(acc_bal)
        fee = client.get_fee_rates(
            symbol=symbol,
        )
        taker = float(fee['result']['list'][0]['takerFeeRate'])*100
        # maker = float(fee['result']['list'][0]['makerFeeRate'])*100
        maker = 0
        # print(maker)
        # print(taker)
        cost = acc_bal - acc_bal*taker - acc_bal*maker
        # print(cost)
        # Calculate quantity
        qty = (cost * float(leverage)* CAPITAL_PERCENTAGE) / (entry_price)
        # print(qty)


        # Place limit order at entry price
        order_response = place_order(symbol, side, qty, order_type="Limit", price=entry_price, take_profit=exit_price, stop_loss=stop_loss_price)
        
        if order_response['retCode'] == 0:
            order_id = order_response['result']['orderId']
            # set_stop_loss(symbol, side, 1, stop_loss_price)  # Assuming qty is 1 for simplicity
            # monitor_market_price(symbol, exit_price, order_id)  # Monitor market price to close position
            return order_response
        else:
            raise Exception("Order placement failed: " + json.dumps(order_response))
    except Exception as e:
        # log_message(f"Error executing trade: {e}")
        raise

def handle_null_signal():
    try:
        response = client.get_positions(category='linear')
        # log_message(f"Positions response: {response}")
        positions = response["result"]
        for position in positions:
            if float(position["size"]) > 0:
                close_positions(position["symbol"])
    except Exception as e:
        # log_message(f"Error handling null signal: {e}")
        raise

def round_qty(qty, step):
    return (qty / step).quantize(Decimal('1'), rounding=ROUND_DOWN) * step