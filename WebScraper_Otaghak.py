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
pn = int(input("Enter the page numbers to Scrape: "))
codts = int(input("How many Ads you want to Scrap?  "))
for page in range(1,pn+1):
    url = f"https://www.otaghak.com/province/gilan/?page={page}"
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
    
    for linkdata in villa_more_info_links:
        
        if count == codts:
                break
        count += 1
        #setting selenium options for request to the site (because of security reasons)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        driver = webdriver.Chrome(options=options)
        driver.get(linkdata)
        #waiting to load the HTML file
        print("waiting for 5 seconds...")
        time.sleep(5)
        

        html = driver.page_source
        soup2 = BeautifulSoup(html, "lxml")
        
        driver.quit()
        price_every_night = soup2.find("div", class_="CtaPrice_basePrice__dlYJ_")
        structure_info = soup2.find_all("div", class_="flex flex-col gap-1 md:gap-2 p-4", id="AboutRoom")
        with open("data_Otaghak.txt", "a", encoding="utf-8") as f: # You can change the directory here
            for tag in structure_info:
                f.write("Villa Name:  "+villa_name.text+"\n")
                f.write("Every Night Price is:  "+str(price_every_night.text)+"\n")
                f.write("All Information:  "+tag.get_text(strip=True)+"\n")
                f.write("More Info In:  "+linkdata+"\n")
                f.write(50*"=="+"\n")
                print(f"AD Number {count} is finished")
                print(50*"==")
