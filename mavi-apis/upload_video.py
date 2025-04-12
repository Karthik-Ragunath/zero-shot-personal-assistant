import requests
import os
from dotenv import load_dotenv
import argparse

load_dotenv(dotenv_path=".env")

# Set up argument parser
parser = argparse.ArgumentParser(description='Upload video to MAVI API')
parser.add_argument('--video', '-v', type=str, required=True, help='Path to video file')
parser.add_argument('--name', '-n', type=str, help='Name for the video (defaults to filename)')
args = parser.parse_args()
# Get video path and name
video_path = args.video
video_name = args.name if args.name else os.path.basename(video_path)

headers = {"Authorization": os.getenv("MAVI_API_KEY")}  # API key  

# Update video file details
data = {
    "file": (video_name, open(video_path, "rb"), "video/mp4")
} 

# # Optional callback URL for task status notifications  
# params = {"callBackUri": "<YOUR_CALLBACK_URI>"}  

response = requests.post(  
    "https://mavi-backend.openinterx.com/api/serve/video/upload",  
    files=data,  
    # params=params,  
    headers=headers  
)  

print(response.json())  