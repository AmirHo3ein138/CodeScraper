import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Step 1: Fetch data from the API
def fetch_api_data():
    url = "https://ws.alibaba.ir/api/v2/accommodation/Available/Search"
    pages = 2
    all_results = []

    for page in range(1, pages + 1):
        payload = {
            "location": "province-gilan",
            "filters": {
                "isInstant": False,
                "capacity": 5,
                "platform": "desktop",
                "title": ["استان گیلان"],
                "amenities": [],
                "scores": [],
                "accommodationTypes": [],
                "guarantees": False
            },
            "date": {
                "startTime": {
                    "seconds": 1746390600,
                    "nanos": 0
                },
                "endTime": {
                    "seconds": 1746477000,
                    "nanos": 0
                }
            },
            "pageNumber": page,
            "pageSize": 16
        }

        headers = {
            "ab-alohomora": "nmaQpMgetUBehdi7Kr9uNq",
            "ab-channel": "WEB-NEW,PRODUCTION,CSR,www.alibaba.ir,desktop,Chrome,135.0.0.0,N,N,Windows,10,3.148.1",
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.alibaba.ir",
            "referer": "https://www.alibaba.ir/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "tracing-device": "N,Chrome,135.0.0.0,N,N,Windows",
            "tracing-sessionid": "1744966597316",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"Page {page} fetched successfully")
            all_results.append(result)
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
            print(response.text)

    with open("result_from_api.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)

    print("All results saved successfully in 'result_from_api.json'")

# Scrape villa details from a predefined URL
def scrape_villas():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)


    url = r"https://www.alibaba.ir/accommodation/search?title=%D8%A7%D8%AC%D8%A7%D8%B1%D9%87+%D9%88%DB%8C%D9%84%D8%A7+%D9%88+%D8%B3%D9%88%D8%A6%DB%8C%D8%AA+%D8%AF%D8%B1+%DA%AF%DB%8C%D9%84%D8%A7%D9%86&checkin=1404-02-15&checkout=1404-02-16&count=5&destination=province-gilan"
    driver.get(url)
    scroll = int(input("Scroll Number: "))
    sleep_time = int(input("Sleep Time: "))
    for _ in range(scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
    print(f"waiting for {sleep_time} seconds... \n Scrolling Down to Load More ADs")
    time.sleep(sleep_time)

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
            f.write(50 * "==" + "\n\n")
    print(f"{count} Numbers of ADs Scraped.")
    driver.quit()

#Scrape villa details using generated links
def scrape_links_from_codes():

    with open("result_from_api.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    all_codes = []

    for page in data:
        items = page.get("result", {}).get("items", [])
        for item in items:
            if "code" in item:
                all_codes.append(item["code"])
    
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    driver = webdriver.Chrome(options=options)

    all_info_links = []
    for code in all_codes:
        link = f"https://www.alibaba.ir/accommodation/pdp/villa-{code}?checkin=1404-02-15&checkout=1404-02-16&count=5&city=province-gilan"
        all_info_links.append(link)    
    
    for link in all_info_links:
        driver.get(link)
        time.sleep(2)  # Wait for the page to load

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        villaa_name = soup.find("h1", class_="font-bold text-7 mt-0")
        villaa_price = soup.find("strong", class_="text-secondary-400")
        villa_functionality = soup.find_all("div", class_="hotel-facility")
        villa_header = soup.find_all("div", class_="header-item")
        villa_content = soup.find("div", class_="text-content")

        if villaa_name:
            villaa_name = villaa_name.text.strip()
        else:
            villaa_name = "N/A"

        if villaa_price:
            villaa_price = villaa_price.text.strip()
        else:
            villaa_price = "N/A"

        if villa_functionality and villa_header and villa_content:
            with open("alldata_Alibaba_links.txt", "a", encoding="utf-8") as f:
                f.write(f"Villa Name: {villaa_name}\n")
                f.write(f"Villa Price: {villaa_price}\n")
                f.write("Functionality: \n")
                for functionality in villa_functionality:
                    f.write(f"{functionality.text.strip()} , ")
                f.write("\nHeaders: \n")
                for header in villa_header:
                    f.write(f"{header.text.strip()} , ")
                f.write(f"\nVilla Info: \n{villa_content.text.strip()}\n")
                f.write(50 * "==" + "\n\n")
    print("Scraping completed.")
    driver.quit()

# Main function to combine all steps
def main():
    fetch_api_data()
    #scrape_villas() #for more data scraping uncomment this line
    scrape_links_from_codes()

if __name__ == "__main__":
    main()
