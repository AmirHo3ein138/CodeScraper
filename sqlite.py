import sqlite3
import re


conn = sqlite3.connect("villa_ads.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS ads (
    ad_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    name TEXT,
    price TEXT,
    owner TEXT,
    description TEXT,
    features TEXT,
    url TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS similar_ads (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ad1_id INTEGER,
    ad2_id INTEGER,
    similarity REAL,
    FOREIGN KEY (ad1_id) REFERENCES ads(ad_id),
    FOREIGN KEY (ad2_id) REFERENCES ads(ad_id)
)
''')

conn.commit()

def extract_ads_from_block(block):
    ads = block.strip().split("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if len(ads) != 2:
        return None

    def parse_ad(text):
        name = re.search(r"Villa Name:\s*(.*)", text)
        price = re.search(r"(?:Every Night Price is:|Villa Price:)\s*(.*)", text)
        owner = re.search(r"(?:Villa Owner:|Villa Owner is:)\s*(.*)", text)
        url = re.search(r"(?:More Info In:|More Information.*?:)\s*(https?://\S+)", text)
        features = re.search(r"(?:Functinalities|Functionality):\s*(.*?)\n(?:Headers:|Villa Info:|More Info|$)", text, re.DOTALL)

        return {
            "name": name.group(1).strip() if name else "",
            "price": price.group(1).strip() if price else "",
            "owner": owner.group(1).strip() if owner else "",
            "url": url.group(1).strip() if url else "",
            "features": features.group(1).replace("\n", "").strip() if features else "",
            "description": text.strip()
        }

    ad1 = parse_ad(ads[0])
    ad2 = parse_ad(ads[1])
    return ad1, ad2

def insert_ad(ad, source):
    cursor.execute('''
        INSERT INTO ads (source, name, price, owner, description, features, url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (source, ad["name"], ad["price"], ad["owner"], ad["description"], ad["features"], ad["url"]))
    return cursor.lastrowid

with open("similarity.txt", "r", encoding="utf-8") as file:
    content = file.read()

matches = re.split(r"=+\n", content)
for match in matches:
    sim = re.search(r"Matched \(([\d.]+)%\)", match)
    if sim:
        similarity = float(sim.group(1))
        ads = extract_ads_from_block(match)
        if ads:
            ad1_id = insert_ad(ads[0], "site1")
            ad2_id = insert_ad(ads[1], "site2")
            cursor.execute('''
                INSERT INTO similar_ads (ad1_id, ad2_id, similarity)
                VALUES (?, ?, ?)
            ''', (ad1_id, ad2_id, similarity))

conn.commit()
conn.close()

print("done")
