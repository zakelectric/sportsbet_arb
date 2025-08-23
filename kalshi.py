import requests

# Replace with the actual MLB series ticker for the markets you want
series_ticker = "KXMLBGAME"  # Example for MLB futures

# Get all open markets for the series
markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={series_ticker}&status=open"
response = requests.get(markets_url)
markets_data = response.json()

print("Active MLB markets:")
for market in markets_data['markets']:
    #print(market)
    print(f"- {market['ticker']}: {market['title']}")
    print(f"  Event: {market['event_ticker']}")
    print(f"  Yes Price: {market['yes_bid']}¢ | Volume: {market['volume']}\n")
