import requests
import json

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
                "seconds": 1745181000,
                "nanos": 0
            },
            "endTime": {
                "seconds": 1745267400,
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

with open(r"D:\All uni data\AP\Webscraping\All MiniProject Data\result_from_api.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print("All results saved successfully in 'result_from_api.json'")
