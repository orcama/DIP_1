import pymongo
import re

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

def clean_text(text):
    text = text.lower()  # Ubah ke huruf kecil
    text = re.sub(r"[^\w\s]", "", text)  # Hapus tanda baca
    text = re.sub(r"\s+", " ", text).strip()  # Hapus spasi berlebih
    return text

print("🟢 Membersihkan data...")

# Hapus komentar kosong
collection.delete_many({"comment_text": {"$eq": ""}})

# Hapus duplikasi berdasarkan ID komentar (jika comment_id tersedia)
if collection.count_documents({"comment_id": {"$exists": True}}) > 0:
    pipeline = [
        {"$group": {"_id": "$comment_id", "doc": {"$first": "$$ROOT"}}},
        {"$replaceRoot": {"newRoot": "$doc"}}
    ]
    cleaned_data = list(collection.aggregate(pipeline))
    collection.delete_many({})
    collection.insert_many(cleaned_data)

# Normalisasi teks di semua komentar
for comment in collection.find():
    if "comment_text" in comment:
        cleaned_text = clean_text(comment.get("comment_text", ""))
        collection.update_one({"_id": comment["_id"]}, {"$set": {"comment_text": cleaned_text}})

print("✅ Data berhasil dibersihkan!")
