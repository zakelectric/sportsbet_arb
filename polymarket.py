import requests

url = " https://data-api.polymarket.com"


response = requests.get(url)
print("RESPONSE", response)
data = response.json()
print("DATA", data)
