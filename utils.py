def log_message(message):
    # with open('trading_bot.log', 'a', encoding='utf-8') as log_file:
    #     log_file.write(f"{message}\n")
    pass

def handle_error(error):
    log_message(f"Error: {error}")

def calculate_position_size(capital, leverage, risk_percentage):
    return (capital * risk_percentage) / leverage

def format_price(price):
    return round(price, 2)

def parse_signal(signal):
    try:
        return {
            "symbol": signal["symbol"],
            "side": signal["side"],
            "price": format_price(signal["price"]),
            "quantity": signal["quantity"]
        }
    except KeyError as e:
        handle_error(f"Missing key in signal: {e}")
        return None