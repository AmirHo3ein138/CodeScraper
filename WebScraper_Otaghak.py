from bs4 import BeautifulSoup
import requests


url = "https://www.otaghak.com/province/gilan/"
new_url = "https://www.otaghak.com"

baseSiteLink = requests.get(url)
soup = BeautifulSoup(baseSiteLink.text, "lxml")

villas = soup.find_all("article", class_="RoomCard_container__FUm8z w-full")
for villa in villas:
    villa_name = villa.find("h2")
    if villa_name:
        print(villa_name.text)
    moreInfo = villa.a["href"]
    moreInfo = new_url  + moreInfo
    print(moreInfo)
