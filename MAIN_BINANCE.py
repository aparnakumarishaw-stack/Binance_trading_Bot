import os
import time
import logging
from dotenv import load_dotenv
from binance.client import Client

# THIS PART ENSURES IT WRITES TO THE FILE
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("trading_bot.log", mode='a'), # 'a' means append to the file
        logging.StreamHandler() # Also shows in your Shell
    ]
)

load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret, testnet=True)

def run_final_test():
    try:
        logging.info("--- NEW SESSION STARTED ---")
        
        # Sync time
        server_time = client.get_server_time()['serverTime']
        local_time = int(time.time() * 1000)
        client.timestamp_offset = server_time - local_time
        logging.info(f"Time synced. Offset: {client.timestamp_offset}ms")

        # Check Balance
        acc = client.futures_account()
        logging.info(f"CONNECTION SUCCESS: Balance is {acc['totalWalletBalance']} USDT")
        
        # Place Order
        logging.info("Placing Market Buy Order for 0.002 BTC...")
        order = client.futures_create_order(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.002
        )
        logging.info(f"ORDER SUCCESS! Order ID: {order['orderId']}")
        logging.info("--- SESSION FINISHED SUCCESSFULLY ---")

    except Exception as e:
        logging.error(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    run_final_test()
