# import requests

# url = "https://clob.polymarket.com/markets"


# response = requests.get(url)
# print("RESPONSE", response)
# data = response.json()
# print("DATA", data)

# from py_clob_client import py_clob_client
# #print(dir(py_clob_client))

# client = py_clob_client()
# markets = client.get_markets()
# print(markets)

# from py_clob_client.client import ClobClient

# client = ClobClient("https://clob.polymarket.com/")  # Level 0 (no auth)

# ok = client.get_ok()
# results = client.get_markets()

# for market in results['data']:
#     print(market['market_slug'])
    # if 'mlb' in market['market_slug']:
    #     print("\n")
    #     print(market)

import requests
import json

url = "https://gamma-api.polymarket.com/markets"

response = requests.get(url)

# Decode bytes to string if needed
if isinstance(response.content, bytes):
    text = response.content.decode('utf-8')
else:
    text = response.text

# Parse JSON
data = json.loads(text)
for market in data:
    print(market)