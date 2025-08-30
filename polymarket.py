from bs4 import BeautifulSoup
from rapidfuzz import process, fuzz
import json

def scrape_polymarket(driver):

    team = None
    price = None

    url = "https://polymarket.com/sports/mlb/games"
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    page_text = soup.get_text(separator='\n', strip=True)

    # Open and unpack abbreviations
    with open("mlb_teams_abr.json") as file:
        mlb_teams_abr_json = json.load(file)
    mlb_teams_abr = []
    for item in mlb_teams_abr_json:
        mlb_teams_abr.append(item['abbr'])

    for line in page_text.split('\n'):
        print("#:", line)
        match, score, _ = process.extractOne(line, mlb_teams_abr)

        if score > 80:
            print("----------------------- FOUND A TEAM MATCH") ### Looking like I need to change the case to uppercase/lower
            team = match
            continue
        if team:
            if '¢' in line and len(line) < 4:
                print("-------------------------- FOUND A PRICE MATCH")
                price = line
            else:
                team = None
            
        if team and price:
            print("LINE AND PRICE FOUND")
            print("team", team)
            print("price", price)
            input()