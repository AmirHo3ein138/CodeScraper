import json

with open("Search.json", "r", encoding="utf-8") as file:
    data = json.load(file)

all_codes = []
for item in data["result"]["items"]:
    if "code" in item:
        all_codes.append(item["code"])

print("All Codes: ")
print(all_codes)
