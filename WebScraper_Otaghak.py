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
    # ...existing code...
villa_more_info_links = []
villas = soup.find_all("article", class_="RoomCard_container__FUm8z w-full")
for villa in villas:
    villa_name = villa.find("h2")
    moreInfo = villa.a["href"]
    moreInfo = new_url + moreInfo
    villa_more_info_links.append((villa_name.text if villa_name else "Unknown", moreInfo))  # ذخیره هر دو

count = 0

for villa_name, linkdata in villa_more_info_links:  # دریافت هر دو مقدار
    if count == codts:
        break
    count += 1
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)
    driver.get(linkdata)
    print("waiting for 5 seconds...")
    time.sleep(5)

    html = driver.page_source
    soup2 = BeautifulSoup(html, "lxml")
    driver.quit()
    owner_tag = soup2.find("h3", class_="Typography_subtitle3__SUcnB text-Asphalt")
    owner = owner_tag.text if owner_tag is not None else "Unknown"
    price_every_night = soup2.find("div", class_="CtaPrice_basePrice__dlYJ_")
    structure_info = soup2.find_all("div", class_="flex flex-col gap-1 md:gap-2 p-4", id="AboutRoom")
    functinality = soup2.find_all("h3", class_="Typography_body2__i3PIz text-Asphalt")
    with open(r"D:\All uni data\AP\Webscraping\All MiniProject Data\data_Otaghak.txt", "a", encoding="utf-8") as f:
        for tag in structure_info:
            f.write("Villa Name:  "+villa_name+"\n")
            f.write("Every Night Price is:  "+str(price_every_night.text if price_every_night else "Unknown")+"\n")
            f.write(f"Villa Owner: {owner}"+"\n")
            f.write("All Information:  "+tag.get_text(strip=True)+"\n")
            f.write("More Info In:  "+linkdata+"\n")
            f.write("Functinalities:\n")
            for func_tag in functinality:
                f.write("- " + func_tag.get_text(strip=True) + "\n")
            f.write(50*"=="+"\n")
        print(f"AD Number {count} is finished")
        print(50*"==")
