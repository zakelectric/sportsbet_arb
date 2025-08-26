import requests
import json
import pandas as pd

# Polymarket API endpoint for markets (CLOB or gamma-api)
url = "https://gamma-api.polymarket.com/markets"

response = requests.get(url)
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    exit(1)

# Decode and parse JSON
try:
    data = response.json()
except Exception:
    data = json.loads(response.content.decode('utf-8'))

# Some APIs return {"markets": [...]}, others just [...]
markets = data.get("markets", data)

mlb_markets = []
for market in markets:
    # Check for MLB in seriesSlug, category, title, or description
    if (
        'seriesSlug' in market and 'mlb' in str(market['seriesSlug']).lower()
        or 'category' in market and 'mlb' in str(market['category']).lower()
        or 'title' in market and 'mlb' in str(market['title']).lower()
        or 'description' in market and 'mlb' in str(market['description']).lower()
    ):
        mlb_markets.append({
            'id': market.get('id'),
            'title': market.get('title'),
            'category': market.get('category'),
            'endDate': market.get('endDate'),
            'active': market.get('active'),
            'volume': market.get('volume'),
            'outcomes': market.get('outcomes'),
            'outcomePrices': market.get('outcomePrices'),
        })

if not mlb_markets:
    print("No MLB markets found.")
else:
    df = pd.DataFrame(mlb_markets)
    print(df)
    df.to_csv("polymarket_mlb.csv", index=False)
    print("Saved MLB markets to polymarket_mlb.csv")
