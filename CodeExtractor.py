import json

with open("result_from_api.json", "r", encoding="utf-8") as file:
    data = json.load(file)

all_codes = []

for page in data:
    items = page.get("result", {}).get("items", [])
    for item in items:
        if "code" in item:
            all_codes.append(item["code"])

print("All Codes:")
print(all_codes)
