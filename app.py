import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import time

url = "https://www.kalshi.com"

opts = uc.ChromeOptions()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
driver = uc.Chrome(options=opts)
driver.get(url)

input()

# wait for table-like element to appear
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "thead th")))

html = driver.page_source
driver.quit()

# parse same as before
soup = BeautifulSoup(html, "lxml")
page_text = soup.get_text(separator='\n', strip=True)
print(page_text)
print("\n\n\nROWS")
rows = [[c.get_text(strip=True) for c in r.select("td,th")] for r in soup.select("table tbody tr")]
print(rows)
print("\n\n\nHEADER")
header = [h.get_text(strip=True) for h in soup.select("table thead th")]
print("\n\n\nDF")
df = pd.DataFrame(rows, columns=header if header and len(header)==len(rows[0]) else None)