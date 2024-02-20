import requests
from database import currency_collection
import time
import asyncio
import websockets
import json


def is_in_collection(symbol):
    result = currency_collection.find_one({"_id": symbol})
    if result:
        return True
    return False


def extract_all_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        tickers = data['symbols']
        symbols = []
        for ticker in tickers:
            if ticker['status'] == 'TRADING':
                symbols.append(ticker['symbol'])
        return symbols


# def add_simbols():
#     symbols_binance = extract_all_symbols()
#     for symbol in symbols_binance:
#         if is_in_collection(symbol):
#             currency_collection.update_one({'_id': symbol}, {'$set': {'binance': 1}})
#         else:
#             currency_collection.insert_one({'_id': symbol, 'binance': 1})


def get_streams():
    symbols = extract_all_symbols()
    streams = []
    for symbol in symbols:
        streams.append(f'{symbol.lower()}@ticker')
    return streams


async def subscribe_to_streams(streams):
    url = 'wss://stream.binance.com:9443/stream?streams='
    streams = sorted(streams)
    async with websockets.connect(url) as websocket:
        groups = [streams[number_streams[0]:number_streams[1]]]
        for i in range(len(groups)):
            subscribe_request = {
                "method": "SUBSCRIBE",
                "params": groups[i],
                "id": 1
            }
            await websocket.send(json.dumps(subscribe_request))
        response = json.loads(await websocket.recv())
        async for message in websocket:
            data = json.loads(message)
            last_price = data['data']['c']
            symbol = data['data']['s']
            if is_in_collection(symbol):
                currency_collection.update_one({'_id': symbol}, {'$set': {'binance_price': last_price}})
            else:
                currency_collection.insert_one({'_id': symbol}, {'binance_price': last_price})
            print(data)


streams = get_streams()
number_streams = list(map(lambda x: int(x), str(input()).split()))
asyncio.run(subscribe_to_streams(streams[number_streams[0]: number_streams[1]]))
