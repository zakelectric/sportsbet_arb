# Sports Arbitrage Bot

A Python application that monitors sports betting odds from BetUS and Kalshi to identify arbitrage opportunities in MLB games.

## Features

- **BetUS Scraping**: Uses Selenium WebDriver to scrape MLB odds from BetUS sportsbook
- **Kalshi API Integration**: Fetches prediction market data from Kalshi API
- **Arbitrage Detection**: Automatically calculates and identifies profitable arbitrage opportunities
- **Error Handling**: Robust error handling for network failures and browser issues
- **Mock Data Support**: Test mode with mock data for development and testing
- **Continuous Monitoring**: Runs continuously with configurable wait times between checks

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zakelectric/sportsbet_arb.git
cd sportsbet_arb
```

2. Install dependencies:
```bash
pip install undetected-chromedriver selenium pandas beautifulsoup4 fuzzywuzzy rapidfuzz lxml python-Levenshtein requests
```

3. Ensure Chrome browser is installed for web scraping functionality.

## Usage

### Running with Real Data
```bash
python3 app.py
```

### Running with Mock Data (for testing)
```bash
USE_MOCK_DATA=true python3 app.py
```

### Running Tests
```bash
python3 run_tests.py
```

## How It Works

1. **Data Collection**: 
   - Scrapes BetUS MLB page for moneyline and runline odds
   - Fetches Kalshi prediction market data via API
   - Uses fuzzy string matching to align team names between sources

2. **Data Processing**:
   - Converts odds to implied probabilities
   - Merges data from both sources by team name
   - Filters for games with complete data from both teams

3. **Arbitrage Detection**:
   - Calculates optimal betting combinations
   - Identifies opportunities where total implied probability < 1.0
   - Displays detailed results with profit potential

## Data Sources

- **BetUS**: Web scraping of https://www.betus.com.pa/sportsbook/mlb/
- **Kalshi**: API calls to https://api.elections.kalshi.com/trade-api/v2/markets

## Configuration Files

- `mlb_teams.json`: List of MLB team names for BetUS matching
- `mlb_teams_abr.json`: Team name to abbreviation mapping for Kalshi

## Output Example

```
---- MERGED DATAFRAME ----
                   team  gamenumber_betus  ...  moneyline_kalshi
0      New York Yankees                 0  ...              0.65
1        Boston Red Sox                 0  ...              0.35

first team: [{'team': 'Los Angeles Dodgers', 'moneyline_kalshi': 0.4, 'moneyline_betus': 0.5238}]
second team: [{'team': 'San Francisco Giants', 'moneyline_kalshi': 0.48, 'moneyline_betus': 0.5238}]
RESULT (highest first + lowest second): 1.0038
RESULT (lowest first + highest second): 0.9238
*** ARBITRAGE OPPORTUNITY DETECTED! ***
```

## Error Handling

The application gracefully handles:
- Network connectivity issues
- Missing Chrome browser or display environment
- API rate limits or service unavailability
- Invalid or missing data

## Files Structure

- `app.py`: Main application logic and orchestration
- `betus.py`: BetUS web scraping functionality
- `kalshi.py`: Kalshi API integration
- `mock_data.py`: Mock data for testing
- `run_tests.py`: Comprehensive test suite
- `mlb_teams.json`: Team names for fuzzy matching
- `mlb_teams_abr.json`: Team abbreviation mappings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite: `python3 run_tests.py`
5. Submit a pull request

## Legal Notice

This software is for educational purposes only. Always comply with the terms of service of the websites and APIs you interact with. Sports betting may be illegal in your jurisdiction.

## License

This project is licensed under the MIT License.