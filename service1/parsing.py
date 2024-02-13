from mongodb import client
import requests

db = client.crypto
tickers = db.tickers

url = "https://api.binance.com/api/v3/capital/config/getall"
def add_tickers():
    response = requests.get(url)
    print(response.json())
add_tickers()