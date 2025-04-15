from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# URL and Setting Headers
url = "https://www.otaghak.com/province/gilan/"
new_url = "https://www.otaghak.com"
HEADERS = {
    'Accept':'*/*',
    'Accept-encoding':'gzip, deflate, br, zstd',
    'Accept-language':'en-US,en;q=0.9',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'

}
#Request to the site
baseSiteLink = requests.get(url, headers=HEADERS)
# create a bs4 object and HTML text
soup = BeautifulSoup(baseSiteLink.text, "lxml")
villa_more_info_links = []
villas = soup.find_all("article", class_="RoomCard_container__FUm8z w-full")
#iterate to get all villa more info links
for villa in villas:
    villa_name = villa.find("h2")
    moreInfo = villa.a["href"]
    moreInfo = new_url  + moreInfo
    villa_more_info_links.append(moreInfo)
# set a counter to count number of advertisements
count = 0
codts = int(input("How many Ads you want to Scrap?"))
for linkdata in villa_more_info_links:
    if count == codts:
            break
    #setting selenium options for request to the site (because of security reasons)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    driver.get(linkdata)
    #waiting to load the HTML file
    print("waiting for 10 seconds")
    time.sleep(10)
    

    html = driver.page_source
    soup2 = BeautifulSoup(html, "lxml")
    print("===="*50)
    driver.quit()
    structure_info = soup2.find_all("div", class_="flex flex-col gap-1 md:gap-2 p-4", id="AboutRoom")
    with open("data.txt", "a", encoding="utf-8") as f: # You can change the directory here
      for tag in structure_info:
          f.write(tag.get_text(strip=True) + "\n")
          print(50 * "==")
    count += 1
