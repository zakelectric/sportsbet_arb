"""
Mock data for testing when network/browser access is not available
"""
import pandas as pd

def get_mock_betus_data():
    """Return mock BetUS data for testing"""
    data = [
        {
            "team": "New York Yankees",
            "gamenumber_betus": 0,
            "sportsbook": "betus",
            "moneyline_betus": "-150",
            "moneyline_impl_betus": 0.6,
            "runline_betus": "-1½ +120"
        },
        {
            "team": "Boston Red Sox",
            "gamenumber_betus": 0,
            "sportsbook": "betus",
            "moneyline_betus": "+130",
            "moneyline_impl_betus": 0.4348,
            "runline_betus": "+1½ -140"
        },
        {
            "team": "Los Angeles Dodgers",
            "gamenumber_betus": 1,
            "sportsbook": "betus",
            "moneyline_betus": "-110",
            "moneyline_impl_betus": 0.5238,
            "runline_betus": "-1½ +105"
        },
        {
            "team": "San Francisco Giants",
            "gamenumber_betus": 1,
            "sportsbook": "betus",
            "moneyline_betus": "-110",
            "moneyline_impl_betus": 0.5238,
            "runline_betus": "+1½ -125"
        }
    ]
    return pd.DataFrame(data)

def get_mock_kalshi_data():
    """Return mock Kalshi data for testing"""
    data = [
        {
            "team": "New York Yankees",
            "gamenumber_kalshi": 101,
            "sportsbook": "kalshi",
            "moneyline_kalshi": 0.65,  # Higher probability for Yankees
            "runline": "null"
        },
        {
            "team": "Boston Red Sox",
            "gamenumber_kalshi": 101,
            "sportsbook": "kalshi",
            "moneyline_kalshi": 0.35,  # Lower probability for Red Sox  
            "runline": "null"
        },
        {
            "team": "Los Angeles Dodgers",
            "gamenumber_kalshi": 102,
            "sportsbook": "kalshi",
            "moneyline_kalshi": 0.40,  # Lower than BetUS - arbitrage opportunity!
            "runline": "null"
        },
        {
            "team": "San Francisco Giants",
            "gamenumber_kalshi": 102,
            "sportsbook": "kalshi",
            "moneyline_kalshi": 0.48,  # Lower than BetUS - arbitrage opportunity!
            "runline": "null"
        }
    ]
    return pd.DataFrame(data)