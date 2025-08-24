import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from betus import scrape_betus
from kalshi import get_kalshi



def create_driver():
    opts = uc.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return uc.Chrome(options=opts)

def main():

    driver = create_driver()

    betus_df = scrape_betus(driver)
    print(betus_df)

    kalshi_df = get_kalshi()
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

    first_team = {}
    second_team = {}
    for idx, row in merged_df.iterrows():
        team = row["team"]
        first_team[row["team"]] = row["team"]
        first_team[row["moneyline_betus"]] = row["moneyline_impl_betus"]







if __name__ == "__main__":
    main()