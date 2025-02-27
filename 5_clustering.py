import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

print("🟢 Melakukan klastering komentar...")

# Ambil semua komentar yang ada
comments = [comment.get("comment_text", "").strip() for comment in collection.find() if comment.get("comment_text")]

if len(comments) < 3:
    print("❌ Jumlah komentar terlalu sedikit untuk clustering.")
else:
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(comments)

    # Tentukan jumlah klaster (misal: 3)
    num_clusters = min(3, len(comments))  # Pastikan jumlah klaster tidak lebih banyak dari data
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    kmeans.fit(X)

    # Simpan hasil klaster ke database
    for i, comment in enumerate(collection.find()):
        if "comment_text" in comment and comment["comment_text"].strip():  # Pastikan ada komentar
            collection.update_one({"_id": comment["_id"]}, {"$set": {"cluster": int(kmeans.labels_[i])}})

    print("✅ Klastering selesai!")

    # Lihat jumlah komentar di tiap klaster
    cluster_counts = np.bincount(kmeans.labels_)
    for i, count in enumerate(cluster_counts):
        print(f"Klaster {i}: {count} komentar")
