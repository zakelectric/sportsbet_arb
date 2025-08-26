import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from betus import scrape_betus
from kalshi import get_kalshi
from mock_data import get_mock_betus_data, get_mock_kalshi_data
import time
import os



def create_driver():
    try:
        opts = uc.ChromeOptions()
        opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        opts.add_argument("--headless=new")  # Enable headless mode for server environments
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        return uc.Chrome(options=opts)
    except Exception as e:
        print(f"Error creating Chrome driver: {e}")
        print("This might be due to missing Chrome browser or display environment")
        return None

def main():

    # Check if we should use mock data
    use_mock_data = os.environ.get('USE_MOCK_DATA', 'false').lower() == 'true'
    
    if use_mock_data:
        print("Using mock data for testing...")
        while True:
            print("Starting sports arbitrage data collection with mock data...")
            
            betus_df = get_mock_betus_data()
            print("----- BETUS DATAFRAME (MOCK) -----")
            print(betus_df)

            kalshi_df = get_mock_kalshi_data()
            print("---- KALSHI DATAFRAME (MOCK) ----")
            print(kalshi_df)

            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)

            merged_df = pd.merge(
                betus_df,
                kalshi_df,
                on="team",         # merge only where "team" matches
                how="inner",       # only rows with matching teams in both DataFrames
                suffixes=("_betus", "_kalshi")
            )
            print("---- MERGED DATAFRAME ----")
            print(merged_df)

            if merged_df.empty:
                print("No matching teams found between BetUS and Kalshi data.")
            else:
                # Process the arbitrage calculations
                process_arbitrage_opportunities(merged_df)
            
            wait = 60 * 5  # Wait 5 minutes in mock mode
            print(f"Waiting {wait} seconds before next iteration...")
            time.sleep(wait)
    else:
        # Original logic with real data
        run_with_real_data()

def process_arbitrage_opportunities(merged_df):
    """Process arbitrage opportunities from merged dataframe"""
    # Filter out rows where gamenumber_betus or gamenumber_kalshi occurs only once
    betus_counts = merged_df["gamenumber_betus"].value_counts()
    kalshi_counts = merged_df["gamenumber_kalshi"].value_counts()

    filtered_df = merged_df[
        (merged_df["gamenumber_betus"].map(betus_counts) > 1) &
        (merged_df["gamenumber_kalshi"].map(kalshi_counts) > 1)
    ]

    print("---- FILTERED DATAFRAME ----")
    print(filtered_df)

    if filtered_df.empty:
        print("No games with multiple teams found after filtering.")
        return

    first_team = []
    second_team = []
    gamenumber_list_kalshi = []
    gamenumber_list_betus = []

    for idx, row in filtered_df.iterrows():
        gamenumber_list_betus.append(row['gamenumber_betus'])
        gamenumber_list_kalshi.append(row['gamenumber_kalshi'])
        #print(f"DEBUG - gamenumber_list_betus: {gamenumber_list_betus} gamenumber_list_kalshi: {gamenumber_list_kalshi}")

        data = {
            "team": row["team"],
            "moneyline_kalshi": row["moneyline_kalshi"],
            "moneyline_betus": row["moneyline_impl_betus"]
        }

        if len(gamenumber_list_betus) == 1:
            first_team.append(data)
        if len(gamenumber_list_betus) == 2:
            second_team.append(data)

        if first_team and second_team:
            if gamenumber_list_betus[0] == gamenumber_list_betus[1] and gamenumber_list_kalshi[0] == gamenumber_list_kalshi[1]:
                #print("Debug: first and second team loaded")
                print("\nfirst team:", first_team)
                print("second team:", second_team)
                moneylines_first = [first_team[-1]["moneyline_kalshi"], first_team[-1]["moneyline_betus"]]
                highest_first = max(moneylines_first)
                lowest_first = min(moneylines_first)

                moneylines_second = [second_team[-1]["moneyline_kalshi"], second_team[-1]["moneyline_betus"]]
                highest_second = max(moneylines_second)
                lowest_second = min(moneylines_second)

                result = highest_first + lowest_second
                print("RESULT (highest first + lowest second):", result)
                result = lowest_first + highest_second
                print("RESULT (lowest first + highest second):", result)

                # Check for arbitrage opportunity
                if result < 1.0:
                    print("*** ARBITRAGE OPPORTUNITY DETECTED! ***")
                else:
                    print("No arbitrage opportunity found.")

                first_team = []
                second_team = []
            else:
                first_team = []
                second_team = []
        
        if len(gamenumber_list_betus) == 2:
            gamenumber_list_kalshi = []
            gamenumber_list_betus = []

def run_with_real_data():
    """Run with real data sources"""
    while True:
        print("Starting sports arbitrage data collection...")
        
        driver = create_driver()
        if driver is None:
            print("Failed to create browser driver. Exiting.")
            break
            
        try:
            betus_df = scrape_betus(driver)
            print("----- BETUS DATAFRAME -----")
            print(betus_df)

            kalshi_df = get_kalshi()
            print("---- KALSHI DATAFRAME ----")
            print(kalshi_df)

            # Check if we have data from both sources
            if betus_df.empty and kalshi_df.empty:
                print("No data available from either source. Skipping this iteration.")
                driver.quit()
                wait = 60 * 5  # Wait 5 minutes instead of 30
                print(f"Waiting {wait} seconds before next attempt...")
                time.sleep(wait)
                continue
            elif betus_df.empty:
                print("No data from BetUS. Skipping merge.")
                driver.quit()
                wait = 60 * 5
                print(f"Waiting {wait} seconds before next attempt...")
                time.sleep(wait)
                continue
            elif kalshi_df.empty:
                print("No data from Kalshi. Skipping merge.")
                driver.quit()
                wait = 60 * 5
                print(f"Waiting {wait} seconds before next attempt...")
                time.sleep(wait)
                continue

            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)

            merged_df = pd.merge(
                betus_df,
                kalshi_df,
                on="team",         # merge only where "team" matches
                how="inner",       # only rows with matching teams in both DataFrames
                suffixes=("_betus", "_kalshi")
            )
            print("---- MERGED DATAFRAME ----")
            print(merged_df)

            if merged_df.empty:
                print("No matching teams found between BetUS and Kalshi data.")
                driver.quit()
                wait = 60 * 10
                print(f"Waiting {wait} seconds before next attempt...")
                time.sleep(wait)
                continue

            # Process the arbitrage calculations
            process_arbitrage_opportunities(merged_df)

        except Exception as e:
            print(f"Error during processing: {e}")
        finally:
            if driver:
                driver.quit()
            
        wait = 60 * 30
        print(f"Waiting {wait} seconds before next iteration...")
        time.sleep(wait)

if __name__ == "__main__":
    main()