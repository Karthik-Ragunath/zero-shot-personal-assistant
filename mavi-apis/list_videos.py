import requests 
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

headers = {"Authorization": os.getenv("MAVI_API_KEY")}  # API key  

# Uncomment the following line to apply filters:  
# This filter retrieves parsed videos uploaded between timestamps 1740995860114 and 1740995860115,  
# returning up to 100 results on the first page.  
# params = {"startTime": 1740995860114, "endTime": 1740995860115, "videoStatus": "PARSE", "page": 1, "pageSize": 100}  

response = requests.get(  
    "https://mavi-backend.openinterx.com/api/serve/video/searchDB",  
    headers=headers  
)

print(response.json())  