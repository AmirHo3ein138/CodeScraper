from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


with open("all_otaghak_villa_data.txt", "r", encoding="utf-8") as f1:
    ads1 = f1.read().split("==================================================")

with open("alldata_Alibaba_links.txt", "r", encoding="utf-8") as f2:
    ads2 = f2.read().split("====================================================================================================")


ads1 = [ad.strip() for ad in ads1 if ad.strip()]
ads2 = [ad.strip() for ad in ads2 if ad.strip()]


vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(ads1 + ads2)
tfidf1 = tfidf[:len(ads1)]
tfidf2 = tfidf[len(ads1):]

similarity_matrix = cosine_similarity(tfidf1, tfidf2)


threshold = 10
matches = []

for i in range(len(ads1)):
    for j in range(len(ads2)):
        score = similarity_matrix[i][j] * 100
        if score >= threshold:
            matches.append((ads1[i], ads2[j], round(score, 2)))


for match in matches:
    with open(r"similarity.txt", "a", encoding="utf-8") as f:
        f.write(f"Matched ({match[2]}%):\n- {match[0][:60]}...\n- {match[1][:60]}...\n")
        f.write(50*"=="+"\n")
