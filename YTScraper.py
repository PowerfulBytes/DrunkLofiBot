from googleapiclient.discovery import build
import json, sys

# Set up the YouTube Data API
api_key = 'AIzaSyDlVZfyam-zX5WdnQhEzPaUGxm3St9A1X4'
youtube = build('youtube', 'v3', developerKey=api_key)

# Get the genre from the command-line arguments
genre = sys.argv[1] if len(sys.argv) > 1 else '24_7 Lofi'

# Define the search parameters
search_keyword = genre
max_results = 50

# Send a search request to the YouTube Data API
request = youtube.search().list(
    part="snippet",
    maxResults=max_results,
    q=search_keyword,
    type="video"
)
response = request.execute()

# Open the output file with utf-8 encoding
with open(f"{genre}.txt", "w", encoding="utf-8") as f:
    # For each search result
    for item in response['items']:
        # Get the video title and URL
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"

        # Write the title and URL to the output file
        f.write(f"{title}: {url}\n")
