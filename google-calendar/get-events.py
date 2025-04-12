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
    
    # Get current local time
    now = datetime.datetime.now()
    
    # Get the start and end of today in local timezone
    # Time zone aware times with 'Z' suffix will be interpreted correctly by Google Calendar API
    today = now.date()
    start_of_day = datetime.datetime.combine(today, datetime.time.min).isoformat() + 'Z'
    end_of_day = datetime.datetime.combine(today, datetime.time.max).isoformat() + 'Z'
    
    print(f"Getting events for {today.strftime('%Y-%m-%d')} (local time)")
    print(f"Start time: {start_of_day}, End time: {end_of_day}")
    
    # First, list available calendars
    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get('items', [])
    
    if not calendars:
        print("No calendars found.")
        return
    
    print("\nAvailable calendars:")
    for calendar in calendars:
        print(f"- {calendar['summary']} (ID: {calendar['id']})")
    
    print("\nEvents from primary calendar:")
    
    # Call the Calendar API with more event fields
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy='startTime',
        maxResults=100,  # Increase to get more events
        fields='items(id,summary,start,end,status)'  # Only fetch needed fields
    ).execute()
    
    events = events_result.get('items', [])
    
    if not events:
        print("No events found for today.")
        return
    
    # Print events as name => ID
    for event in events:
        event_name = event.get('summary', 'Untitled Event')
        event_id = event['id']
        start_time = event['start'].get('dateTime', event['start'].get('date', 'All day'))
        status = event.get('status', 'Unknown')
        print(f"{event_name} [{status}] => {event_id}")
        print(f"  Starts: {start_time}")

if __name__ == '__main__':
    get_todays_events()