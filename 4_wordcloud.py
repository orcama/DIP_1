import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Koneksi ke MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["youtube_data"]
collection = db["comments"]

print("🟢 Membuat Word Cloud...")

# Gabungkan semua komentar menjadi satu teks besar
all_text = " ".join(comment.get("comment_text", "").strip() for comment in collection.find() if comment.get("comment_text"))

# Generate Word Cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_text)

# Tampilkan Word Cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud Komentar YouTube")
plt.show()
