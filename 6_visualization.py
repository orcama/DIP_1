import pymongo
import matplotlib.pyplot as plt

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

print("🟢 Membuat visualisasi sentimen...")

# Ambil jumlah komentar berdasarkan sentimen
sentiment_counts = collection.aggregate([
    {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
])

# Konversi hasil ke dictionary
sentiment_data = {s["_id"]: s["count"] for s in sentiment_counts}

# Pastikan semua kategori ada (agar grafik tidak error jika ada yang kosong)
categories = ["Positif", "Negatif", "Netral"]
values = [sentiment_data.get(cat, 0) for cat in categories]

# Cek apakah ada data untuk divisualisasikan
if sum(values) == 0:
    print("❌ Tidak ada data sentimen untuk divisualisasikan.")
else:
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # **1️⃣ Bar Chart - Jumlah Sentimen**
    axs[0].bar(categories, values, color=["green", "red", "gray"])
    axs[0].set_xlabel("Sentimen")
    axs[0].set_ylabel("Jumlah Komentar")
    axs[0].set_title("Analisis Sentimen Komentar YouTube")
    
    # Tambahkan angka di atas batang grafik
    for i, v in enumerate(values):
        axs[0].text(i, v + 0.5, str(v), ha="center", fontsize=10)

    # **2️⃣ Pie Chart - Proporsi Sentimen**
    axs[1].pie(values, labels=categories, autopct="%1.1f%%", colors=["green", "red", "gray"], startangle=140)
    axs[1].set_title("Distribusi Sentimen Komentar")

    plt.tight_layout()
    plt.show()
