import pymongo
from textblob import TextBlob

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

print("🟢 Melakukan analisis sentimen...")

for comment in collection.find():
    text = comment.get("comment_text", "").strip()  # Pastikan mengambil comment_text, bukan text
    
    if text:  # Hanya proses jika ada komentar
        sentiment_score = TextBlob(text).sentiment.polarity  # Skor -1 (negatif) ke 1 (positif)

        sentiment = "Netral"
        if sentiment_score > 0:
            sentiment = "Positif"
        elif sentiment_score < 0:
            sentiment = "Negatif"

        # Simpan hasil ke database
        collection.update_one({"_id": comment["_id"]}, {"$set": {"sentiment": sentiment}})

print("✅ Analisis sentimen selesai!")
