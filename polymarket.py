# import json

# import requests

# # Get markets
# markets = requests.get("https://gamma-api.polymarket.com/markets")
# print(markets.json())

# # Get events
# events = requests.get("https://gamma-api.polymarket.com/events")
# json_data = json.dumps(events.json(), indent=4)
# with open("events.json", "w") as file:
#     file.write(json_data)
# print(
#     "Data formatted and saved to events.json, look for clobTokenIds later in this tutorial"
# )

from bs4 import BeautifulSoup


def scrape_polymarket(driver):

    url = "https://polymarket.com/sports/mlb/games"
    driver.get(url)

    #time.sleep(15)

    rows = []
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    page_text = soup.get_text(separator='\n', strip=True)

    print(page_text)