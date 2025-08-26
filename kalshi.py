import requests
import pandas as pd
import json
from rapidfuzz import process, fuzz
import os


def get_kalshi():
    
    series_ticker = "KXMLBGAME"
    markets_url = f"https://api.elections.kalshi.com/trade-api/v2/markets?series_ticker={series_ticker}&status=open"
    
    try:
        response = requests.get(markets_url, timeout=10)
        response.raise_for_status()
        markets_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Kalshi API: {e}")
        print("Returning empty DataFrame")
        return pd.DataFrame(columns=["team", "gamenumber_kalshi", "sportsbook", "moneyline_kalshi", "runline"])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response from Kalshi API: {e}")
        print("Returning empty DataFrame")
        return pd.DataFrame(columns=["team", "gamenumber_kalshi", "sportsbook", "moneyline_kalshi", "runline"])

    rows = []
    last_game = None
    game_number = 100

    try:
        with open(os.path.join(os.path.dirname(__file__), "mlb_teams_abr.json")) as f:
            mlb_teams = json.load(f)
    except FileNotFoundError:
        print("Warning: mlb_teams_abr.json not found, using empty team mapping")
        mlb_teams = []

    abbr_to_name = {}
    abbr_choices = []
    for item in mlb_teams:
        abbr = item.get("abbr")
        name = item.get("name")
        if abbr:
            abbr_to_name[abbr] = name
            abbr_choices.append(abbr)

    # Check if markets_data has the expected structure
    if not isinstance(markets_data, dict) or 'markets' not in markets_data:
        print("Warning: Unexpected API response structure")
        return pd.DataFrame(columns=["team", "gamenumber_kalshi", "sportsbook", "moneyline_kalshi", "runline"])

    print("Active MLB markets:")
    for market in markets_data['markets']:
        print(f"- {market['ticker']}: {market['title']}")
        print(f"  Event: {market['event_ticker']}")
        print(f"  Yes Price: {market['yes_bid']}¢ | No Price: {market['no_bid']}¢ | Volume: {market['volume']}\n")

        if market['title'] != last_game:
            game_number += 1

        yes_bid_decimal = market['yes_bid'] * .01

        # extract last 3 chars of ticker and fuzzy-match against abbr list
        raw_abbr = market['ticker'][-3:]
        if "-" in raw_abbr:
            sanitized_abbr = raw_abbr.replace('-', '')
        else:
            sanitized_abbr = raw_abbr
        team_name = None
        matched_abbr = sanitized_abbr

        if abbr_choices:
            best = process.extractOne(sanitized_abbr, abbr_choices, scorer=fuzz.ratio)
            if best:
                choice, score, _ = best  # (match, score, index)
                if score >= 85:
                    matched_abbr = choice
                    team_name = abbr_to_name.get(choice)

        # fallback: if no mapping found, keep raw abbr as team value
        team_value = team_name if team_name else matched_abbr

        row = {
            "team": team_value,
            "gamenumber_kalshi": game_number,
            "sportsbook": "kalshi",
            "moneyline_kalshi": yes_bid_decimal,
            "runline": "null"
        }
        rows.append(row)
        last_game = market['title']

    df = pd.DataFrame(rows, columns=["team", "gamenumber_kalshi", "sportsbook", "moneyline_kalshi", "runline"])

    return df

