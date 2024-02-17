from config import API_KEY_CoinMarket
from database import client
import requests
import json

db = client.cryptoDB
collection = db.cryptocurrency
key = API_KEY_CoinMarket
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
    'id': 1
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)['data']


def is_in_db(symbol):
    result = collection.find_one({"_id": symbol})
    if result:
        return True
    return False

for crypto in data:
    symbol = crypto['symbol']
    if not is_in_db(symbol):
        collection.insert_one({'_id': symbol})

