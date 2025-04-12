import requests
from dotenv import load_dotenv
import os
import argparse
load_dotenv(dotenv_path=".env")

headers = {"Authorization": os.getenv("MAVI_API_KEY")}  # API key  
# Set up argument parser
parser = argparse.ArgumentParser(description='Get transcription task status from MAVI API')
parser.add_argument('--task-no', '-t', type=str, required=True, help='Task number to check status for')
args = parser.parse_args()

task_no = args.task_no

# Task number associated with the transcription request  
params = {"taskNo": task_no}  

response = requests.get(  
    "https://mavi-backend.openinterx.com/api/serve/video/getTranscription",  
    headers=headers,  
    params=params  
)  

print(response.json()) 