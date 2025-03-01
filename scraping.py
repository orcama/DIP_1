import os
import googleapiclient.discovery

def get_video_id(video_url):
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
        return video_url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def scrape_youtube_comments(video_url, api_key, output_file="comments.txt"): 
    video_id = get_video_id(video_url)
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    
    while request:
        response = request.execute()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
        
        request = youtube.commentThreads().list_next(request, response)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for comment in comments:
            f.write(comment + "\n")
    
    print(f"Scraping selesai! Komentar disimpan di {output_file}")

if __name__ == "__main__":
    API_KEY = "AIzaSyCriCiPB5IhxESmyh3XPuiuz1Q1xHsGtX0"
    VIDEO_URL = input("Masukkan link video YouTube: ")
    scrape_youtube_comments(VIDEO_URL, API_KEY)
