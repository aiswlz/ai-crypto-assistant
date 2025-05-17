from binance.client import Client
import os

client = Client()

def get_crypto_price(symbol="BTC"):
    try:
        price = client.get_symbol_ticker(symbol=f"{symbol}USDT")
        return float(price["price"])
    except Exception as e:
        print(f"Binance API Error: {e}")
        return 0.0