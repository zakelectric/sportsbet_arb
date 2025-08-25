import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from betus import scrape_betus
from kalshi import get_kalshi
import time



def create_driver():
    opts = uc.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    #opts.add_argument("--headless=new") 
    return uc.Chrome(options=opts)

def main():

    while True:
        driver = create_driver()
        betus_df = scrape_betus(driver)
        print("----- BETUS DATAFRAME -----")
        print(betus_df)

        kalshi_df = get_kalshi()
        print("---- KALSHI DATAFRAME ----")
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
        print(merged_df)

        # Filter out rows where gamenumber_betus or gamenumber_kalshi occurs only once
        betus_counts = merged_df["gamenumber_betus"].value_counts()
        kalshi_counts = merged_df["gamenumber_kalshi"].value_counts()

        filtered_df = merged_df[
            (merged_df["gamenumber_betus"].map(betus_counts) > 1) &
            (merged_df["gamenumber_kalshi"].map(kalshi_counts) > 1)
        ]

        print(filtered_df)

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
                    print("RESULT", result)
                    result = lowest_first + highest_second
                    print("RESULT", result)

                    first_team = []
                    second_team = []
                else:
                    first_team = []
                    second_team = []
            
            if len(gamenumber_list_betus) == 2:
                gamenumber_list_kalshi = []
                gamenumber_list_betus = []

        driver.quit()
        wait = 60 * 30
        time.sleep(wait)

if __name__ == "__main__":
    main()