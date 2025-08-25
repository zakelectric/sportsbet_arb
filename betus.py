import pandas as pd
from bs4 import BeautifulSoup
import time
import json
from fuzzywuzzy import process
import re


def scrape_betus(driver):
    moneyline_pattern = r'[+-]\d{3}'
    runline_pattern = r'[+-]\d+½ [+-]\d{3}'
    append_data = False
    moneyline_matches = None
    runline_matches = None
    moneyline = None
    runline = None
    line_counter = 0
    x = 0
    game_number = 0

    def process_moneyline(moneyline):

        moneyline = float(moneyline)

        if moneyline < 0:
            result = abs(moneyline) / (abs(moneyline) + 100)
        else:
            result = 100 / (abs(moneyline) + 100)
        return result

    with open("mlb_teams.json") as f:
        mlb_teams = json.load(f)

    url = "https://www.betus.com.pa/sportsbook/mlb/"
    driver.get(url)
    
    #time.sleep(15)

    rows = []
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    page_text = soup.get_text(separator='\n', strip=True)

    for line in page_text.split('\n'):
        print("#:", line)
        match, score = process.extractOne(line, mlb_teams)
        if score > 80:
            #print(f"Matched team: {match} (score: {score})")
            team = match
            append_data = True
        
        line_counter += 1

        if append_data:

            #print("DEBUG: ------------------------ appending data")

            if runline == None:
                #print("DEBUG: ---------------------- RUNLINE IS NONE")
                runline_matches = re.findall(runline_pattern, line)
                if runline_matches:
                    runline = runline_matches[0]
                    #print(f"Found runline: {runline}")  

            if moneyline == None:
                #print("DEBUG: ------------------------------- MONEYLINE IS NONE")
                cleaned_line = line.strip()
                if len(cleaned_line) > 3 and len(cleaned_line) < 6:
                    moneyline_matches = re.findall(moneyline_pattern, line)
                    if moneyline_matches:
                        moneyline = moneyline_matches[0]
                if 'Ev' in cleaned_line or 'ev' in cleaned_line and len(cleaned_line) == 2:
                    moneyline = '+100'
                        #print(f"Found moneyline: {moneyline}")

            if moneyline and runline:
                print("\n\nBoth moneyline and runline found!") 
                print("Team:", team)
                print("Moneyline", moneyline)
                print("Runline", runline)
                x += 1

                moneyline_impl = process_moneyline(moneyline)

                row = {
                    "team": team,
                    "gamenumber_betus": game_number,
                    "sportsbook": "betus",
                    "moneyline_betus": moneyline,
                    "moneyline_impl_betus": moneyline_impl,
                    "runline_betus": runline
                }
                rows.append(row)

                runline = None
                moneyline = None
            
            if line_counter > 5:
                line_counter = 0
                append_data = False
            if x > 1:
                x = 0
                game_number += 1

    df = pd.DataFrame(rows, columns=["team", "gamenumber_betus", "sportsbook", "moneyline_betus", "moneyline_impl_betus", "runline_betus"])

    return df
                           