import requests
import json

# Fetch API data and extract room IDs
def fetch_and_extract_room_ids():
    url = "https://www.otaghak.com/_next/data/yqQdPm21Hm4fDrwW8LjF9/index.json"
    headers = {
        "https": "",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cookie": "_gcl_au=1.1.1428219628.1744568818; _ga=GA1.1.2032840298.1744568819; analytics_token=f7bf8672-f1ce-cf8d-58d3-da008ee3cf15; _yngt=01JG14SAGN6XA9VYGY5TPEMR99; _ga_QXWTV4ELP3=deleted; token={}; otgk_thread=thread_53mlLnIGcnOpcqnJJvYWreAE; _yngt_iframe=1; analytics_session_token=06167c4c-2751-95b1-7d79-9247175eb8ce; yektanet_session_last_activity=4/30/2025; _clck=19ostbb%7C2%7Cfvi%7C0%7C1929; pageviewCount=45; _clsk=1qfx1iy%7C1746004660792%7C5%7C1%7Cj.clarity.ms%2Fcollect; _ga_QXWTV4ELP3=GS1.1.1746003962.16.1.1746004674.0.0.0",
        "priority": "u=1, i",
        "purpose": "prefetch",
        "referer": "https://www.otaghak.com/province/gilan/",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "x-nextjs-data": "1"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("API data fetched successfully.")
        data = response.json()

        # Save the JSON response to a file
        with open("result_from_otaghak.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Extract room IDs
        all_codes = []
        def extract_room_ids(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == "roomId":
                        all_codes.append(value)
                    else:
                        extract_room_ids(value)
            elif isinstance(obj, list):
                for item in obj:
                    extract_room_ids(item)

        extract_room_ids(data)
        return all_codes
    else:
        print(f"Failed to fetch API data: {response.status_code}")
        print(response.text)
        return []

# Fetch room details using room IDs
def fetch_room_details(all_codes):
    url_template = "https://core.otaghak.com/api/v3/Rooms/GetRoomPdpAttributes?roomId={}&generatedDevice=WebSite"
    headers = {
        "Host": "core.otaghak.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.otaghak.com",
        "Priority": "u=1, i",
        "Referer": "https://www.otaghak.com/",
        "Sec-Ch-Ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    with open("all_villa_data_otaghak.txt", "w", encoding="utf-8") as output_file:
        for idx, room_id in enumerate(all_codes, start=1):
            url = url_template.format(room_id)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                room_data = response.json()
                output_file.write(f"Villa {idx}:\n")
                json.dump(room_data, output_file, indent=2, ensure_ascii=False)
                output_file.write("\n" + "=" * 50 + "\n")
            else:
                print(f"Failed to fetch details for Room ID {room_id}: {response.status_code}")
                print(response.text)

    print("All villa data saved successfully in 'all_villa_data_otaghak.txt'.")

# Extract all "name" and "description" values from the villa data
def extract_name_and_description():
    try:
        # Load the villa data from the file
        with open("all_villa_data_otaghak.txt", "r", encoding="utf-8") as f:
            data = f.read()

        # Split Villa Files
        villas = data.split("=" * 50)

        # Open the output file to save the extracted data
        with open("extracted_villa_data_otaghak.txt", "w", encoding="utf-8") as output_file:
            for idx, villa in enumerate(villas, start=1):
                output_file.write(f"Villa {idx}:\n")
                try:
                    # Remove the "Villa {idx}:" header and clean the JSON part
                    villa_json_start = villa.find("[")
                    if villa_json_start == -1:
                        continue  # Skip if no JSON data is found
                    villa_data = json.loads(villa[villa_json_start:].strip())

                    # Recursive function to extract "name" and "description" values
                    def extract_data(obj):
                        if isinstance(obj, dict):
                            if "name" in obj:
                                output_file.write(f"Name: {obj['name']}\n")
                            if "description" in obj and obj["description"]:
                                output_file.write(f"Description: {obj['description']}\n")
                            for key, value in obj.items():
                                extract_data(value)
                        elif isinstance(obj, list):
                            for item in obj:
                                extract_data(item)

                    extract_data(villa_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for Villa {idx}: {e}")
                output_file.write("=" * 50 + "\n")

        print("All 'name' and 'description' values extracted and saved to 'extracted_villa_data_otaghak.txt'.")
    except FileNotFoundError:
        print("The file 'all_villa_data_otaghak.txt' does not exist. Please ensure the file is available.")

# Main function to combine all Funcs
def main():
    all_codes = fetch_and_extract_room_ids()
    if all_codes:
        fetch_room_details(all_codes)
        extract_name_and_description()

if __name__ == "__main__":
    main()
