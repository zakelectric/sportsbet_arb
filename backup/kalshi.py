import requests
import pandas as pd

# Replace with the actual MLB series ticker for the markets you want
series_ticker = "KXMLBGAME"  # Example for MLB futures

# Get all open markets for the series
markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={series_ticker}&status=open"
response = requests.get(markets_url)
markets_data = response.json()

rows = []
last_game = None
game_number = 0

print("Active MLB markets:")
for market in markets_data['markets']:
    print(f"- {market['ticker']}: {market['title']}")
    print(f"  Event: {market['event_ticker']}")
    print(f"  Yes Price: {market['yes_bid']}¢ | No Price: {market['no_bid']}¢ | Volume: {market['volume']}\n")

    if market['title'] != last_game:
        game_number += 1

    row = {
        "team": market['ticker'][-3:],
        "gamenumber": game_number,
        "sportsbook": "kalshi",
        "moneyline": market['yes_bid'],
        "runline": "null"
    }
    rows.append(row)
    last_game = market['title']

df = pd.DataFrame(rows, columns=["team", "gamenumber", "sportsbook", "moneyline", "runline"])

print(df)

