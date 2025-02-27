import pymongo

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

# Ambil semua data dalam koleksi comments
print("🟢 Daftar semua komentar:")
for comment in collection.find():
    print(comment)
