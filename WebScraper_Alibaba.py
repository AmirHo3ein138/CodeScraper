from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# URL and Setting Headers
url = r"https://www.alibaba.ir/accommodation/search?destination=province-gilan&title=%D8%A7%D8%B3%D8%AA%D8%A7%D9%86+%DA%AF%DB%8C%D9%84%D8%A7%D9%86&checkin=1404-01-30&checkout=1404-01-31&count=5&accommodationTypes=villa"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(options=options)
driver.get(url)
    #waiting to load the HTML file
print("waiting for 10 seconds...")
time.sleep(10)
    

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

villas = soup.find_all("li", class_="a-card mb-4 last:mb-0 cards-flip-item available-card")
count = 0
vnts = int(input("Enter Villa Numbers to Scrap:  "))
for villa in villas:
    if count == vnts:
        break

    count += 1
    villa_name = villa.find("div", class_="available-card__title").text
    villa_price = villa.find("strong", class_="text-6 text-secondary-400").text
    villa_place_info = villa.find("div", class_="available-card__meta__item").text
    with open("data_Alibaba.txt", "a", encoding="utf-8") as f:
        f.write(f"Villa Name is: {villa_name}\n")
        f.write(f"Villa Price for Every Night is: {villa_price}\n")
        f.write(f"Villa Basic Information is: {villa_place_info}\n")
        f.write(50*"===")
        print(f"{count} Numbers of ADs Screaped.")
