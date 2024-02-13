from fastapi import FastAPI
from fastapi.websockets import WebSocket
import asyncio
import websockets
import json

url = 'wss://stream.binance.com:9443/stream?streams='

streams = [
    "btcusdt@ticker"
]


async def subscribe_to_streams():
    async with websockets.connect(url) as websocket:
        subscribe_request = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": 1
        }
        await websocket.send(json.dumps(subscribe_request))
        response = json.loads(await websocket.recv())
        print(response)
        async for message in websocket:
            data = json.loads(message)
            print(data)


asyncio.run(subscribe_to_streams())
