import pymongo

# Konfigurasi koneksi MongoDB
mongo_uri = "mongodb://localhost:27017/"  # Ubah jika menggunakan MongoDB Atlas
db_name = "youtube_data"  # Nama database
collection_name = "comments"  # Nama koleksi (tabel)

# Koneksi ke MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]

def load_to_mongodb(file_path):
    """Fungsi untuk memasukkan data dari file ke MongoDB."""
    with open(file_path, "r", encoding="utf-8") as f:
        comments = [{"comment_text": line.strip()} for line in f if line.strip()]  # Hapus baris kosong
    
    if comments:
        collection.insert_many(comments)
        print(f"{len(comments)} komentar berhasil dimasukkan ke MongoDB!")

# Load data ke MongoDB
load_to_mongodb("comments.txt")
