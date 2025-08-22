import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time
import json
from fuzzywuzzy import process
import re

moneyline_pattern = r'[+-]\d{3}'
runline_pattern = r'[+-]\d+½ [+-]\d{3}'

url = "https://www.betus.com.pa/sportsbook/lines/"

opts = uc.ChromeOptions()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
driver = uc.Chrome(options=opts)
driver.get(url)


def main():
    append_data = False
    moneyline = None
    runline = None
    line_counter = 0

    with open("mlb_teams.json") as f:
        mlb_teams = json.load(f)

    while True:

        html = driver.page_source

        soup = BeautifulSoup(html, "lxml")
        print("Hit ENTER to proceed with scraping...")
        input()

        page_text = soup.get_text(separator='\n', strip=True)

        for line in page_text.split('\n'):
            print("#:", line)
            match, score = process.extractOne(line, mlb_teams)
            if score > 80:
                print(f"Matched team: {match} (score: {score})")
                team = match
                append_data = True
            
            line_counter += 1

            if append_data:

                print("------------------------ appending data")

                if runline == None:
                    print("---------------------- RUNLINE IS NONE")
                    runline = re.findall(runline_pattern, line)

                    print(f"Found runline: {runline}")  

                if moneyline == None:
                    print("------------------------------- MONEYLINE IS NONE")
                    cleaned_line = line.strip()
                    if len(cleaned_line) == 4:
                        moneyline = re.findall(moneyline_pattern, line)
                    
                        print(f"Found moneyline: {moneyline}")

                if moneyline or runline:
                    print("\n\nBoth moneyline and runline found!") 
                    print("Team:", team)
                    print("Moneyline", moneyline)
                    print("Runline", runline)
                    input()                       
                
                if line_counter > 5:
                    line_counter = 0
                    append_data = False
                            


if __name__ == "__main__":
    main()