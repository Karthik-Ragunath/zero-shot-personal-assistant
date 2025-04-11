# Google Calendar Events Script

A script to extract today's events from a user's Google Calendar and output them as a list of event names with their corresponding event IDs.

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up Google Calendar API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Calendar API
   - Create OAuth credentials (Desktop application)
   - Download the credentials.json file and place it in this directory

## Usage

Run the script:
```
python get-events.py
```

On first run, the script will open a browser window asking you to authorize access to your Google Calendar. After authorization, a token.pickle file will be created to store your credentials for future use.

The script will output today's events in the format:
```
Event Name => Event ID
```