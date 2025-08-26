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

from py_clob_client.client import ClobClient

client = ClobClient("https://clob.polymarket.com")  # Level 0 (no auth)

ok = client.get_ok()
results = client.get_markets()

for market in results['data']:
    if 'baseball' in market.get('tags', ''):
        print("\n")
        print(market)