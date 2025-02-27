import pymongo
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import string

# Download tokenizer NLTK
nltk.download("punkt")

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

print("🟢 Menghitung kata yang paling sering muncul...")

word_list = []
for comment in collection.find():
    text = comment.get("comment_text", "").strip()  # Gunakan comment_text, bukan text
    
    if text:  # Hanya proses jika ada komentar
        words = word_tokenize(text.lower())  # Ubah ke huruf kecil dan tokenisasi
        words = [word for word in words if word.isalnum()]  # Hanya ambil kata, bukan tanda baca
        word_list.extend(words)

word_counts = Counter(word_list)
common_words = word_counts.most_common(20)  # Ambil 20 kata paling sering muncul

print("🔍 20 Kata Paling Sering Muncul:")
for word, count in common_words:
    print(f"{word}: {count}")
