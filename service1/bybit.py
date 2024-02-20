from pybit.unified_trading import WebSocket
from time import sleep
from database import currency_collection
import json
import requests


def is_in_collection(symbol):
    result = currency_collection.find_one({"_id": symbol})
    if result:
        return True
    return False


def extract_all_symbols():
    url = "https://api-testnet.bybit.com/v5/market/tickers"
    parameters = {'category': 'linear'}
    headers = {}
    response = requests.request("GET", url, headers=headers, params=parameters)
    data = json.loads(response.text)
    symbols = []
    for ticker in data['result']['list']:
        symbols.append(ticker['symbol'])
    return symbols


symbols = extract_all_symbols()

ws = WebSocket(
    testnet=True,
    channel_type="linear",
)


def update_last_price(message):
    data = message['data']
    symbol = data['symbol']
    last_price = data['lastPrice']
    if is_in_collection(symbol):
        currency_collection.update_one({'_id': symbol}, {'$set': {'bybit_price': last_price}})
    else:
        currency_collection.insert_one({'_id': symbol, 'bybit_price': last_price})


for symbol in symbols:
    ws.ticker_stream(symbol=symbol, callback=update_last_price)

while True:
    sleep(1)
