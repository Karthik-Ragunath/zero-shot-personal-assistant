#!/usr/bin/env python3

import os
import datetime
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Get an authorized Google Calendar API service instance."""
    creds = None
    # The token.pickle file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials don't exist or are invalid, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def get_todays_events():
    """Fetch and display today's events from Google Calendar."""
    service = get_calendar_service()
    
    # Get the start and end of today in UTC format
    today = datetime.datetime.utcnow().date()
    start_of_day = datetime.datetime.combine(today, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(today, datetime.time.max).isoformat() + 'Z'
    
    print(f"Getting events for {today.strftime('%Y-%m-%d')}")
    
    # Call the Calendar API
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print("No events found for today.")
        return
    
    # Print events as name => ID
    for event in events:
        event_name = event['summary']
        event_id = event['id']
        print(f"{event_name} => {event_id}")

if __name__ == '__main__':
    get_todays_events()