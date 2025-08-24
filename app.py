import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from betus import scrape_betus



def create_driver():
    opts = uc.ChromeOptions()
    opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
    return uc.Chrome(options=opts)

def main():

    driver = create_driver()

    betus_df = scrape_betus(driver)

    print(betus_df)

if __name__ == "__main__":
    main()