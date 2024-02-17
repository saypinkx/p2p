from pybit.unified_trading import WebSocket
from time import sleep
from database import currency_collection
import json
import requests


def is_in_db(symbol):
    result = currency_collection.find_one({"_id": symbol})
    if result:
        return True
    return False


def extract_all_symbols_in_collection():
    url = "https://api-testnet.bybit.com/v5/market/tickers"
    parameters = {'category': 'linear'}
    headers = {}
    response = requests.request("GET", url, headers=headers, params=parameters)
    data = json.loads(response.text)
    for ticker in data['result']['list']:
        if not is_in_db(ticker['symbol']):
            currency_collection.insert_one({'_id': ticker['symbol'], 'bybit': 1})


symbols = list(map(lambda x: x['_id'], list(currency_collection.find({'bybit': 1}))))

ws = WebSocket(
    testnet=True,
    channel_type="linear",
)


def update_last_price(message):
    data = message['data']
    symbol = data['symbol']
    last_price = data['lastPrice']
    currency_collection.update_one({'_id': symbol}, {'$set': {'bybit_price': last_price}})


for symbol in symbols:
    ws.ticker_stream(symbol=symbol, callback=update_last_price)

while True:
    sleep(1)

