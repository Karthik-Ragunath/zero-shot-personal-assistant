import requests
import os
from dotenv import load_dotenv
import argparse

load_dotenv(dotenv_path=".env")

headers = {"Authorization": os.getenv("MAVI_API_KEY")}  # API key  
# Set up argument parser
parser = argparse.ArgumentParser(description='Transcribe video audio from MAVI API')
parser.add_argument('--video-no', '-v', type=str, required=True, help='Video number to transcribe')
args = parser.parse_args()

video_no = args.video_no

data = {  
    "videoNo": f"{video_no}",  # The video ID to transcribe  
    "type": "AUDIO",  # Specify "AUDIO" for audio-only, "VIDEO" for video-only, or "AUDIO/VIDEO" for both  
    # "callBackUri": "<CALLBACK>"  # Optional callback URL for status notifications  
}  

response = requests.post(  
    "https://mavi-backend.openinterx.com/api/serve/video/subTranscription",  
    headers=headers,  
    json=data  
)  

print(response.json())
