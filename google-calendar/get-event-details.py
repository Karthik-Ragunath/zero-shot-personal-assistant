#!/usr/bin/env python3

import os
import sys
import json
import datetime
import pickle
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the token.pickle file
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

DEFAULT_EVENT_ID = "148noac90qud46961mpe7i5pjv"

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

def get_event_details(event_id, calendar_id='primary'):
    """
    Fetch detailed information about a specific event by its ID.
    
    Args:
        event_id (str): The ID of the event to retrieve
        calendar_id (str): The calendar ID (default is 'primary')
        
    Returns:
        dict: The event details as a dictionary
    """
    service = get_calendar_service()
    
    try:
        # Get the event details
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        return event
    except Exception as e:
        print(f"Error retrieving event: {e}")
        return None

def format_event_as_markdown(event):
    """
    Format the event details as markdown.
    
    Args:
        event (dict): The event details
        
    Returns:
        str: Markdown formatted event details
    """
    if not event:
        return "## Error\nEvent not found or access denied."
    
    # Start with main event details
    markdown = f"# {event.get('summary', 'Untitled Event')}\n\n"
    
    # Basic information
    markdown += "## Basic Information\n\n"
    markdown += f"- **ID**: `{event.get('id', 'N/A')}`\n"
    markdown += f"- **Status**: {event.get('status', 'N/A')}\n"
    
    # Format the start and end times
    start = event.get('start', {})
    end = event.get('end', {})
    
    start_time = start.get('dateTime', start.get('date', 'N/A'))
    end_time = end.get('dateTime', end.get('date', 'N/A'))
    
    markdown += f"- **Start**: {start_time}\n"
    markdown += f"- **End**: {end_time}\n"
    
    # Handle location
    if 'location' in event:
        markdown += f"- **Location**: {event['location']}\n"
    
    # Handle description
    if 'description' in event:
        markdown += "\n## Description\n\n"
        markdown += event['description'] + "\n"
    
    # Handle attendees
    if 'attendees' in event and event['attendees']:
        markdown += "\n## Attendees\n\n"
        for attendee in event['attendees']:
            response_status = attendee.get('responseStatus', 'N/A')
            display_name = attendee.get('displayName', 'Unknown')
            email = attendee.get('email', 'N/A')
            
            markdown += f"- **{display_name}** ({email}): {response_status}\n"
    
    # Handle organizer
    if 'organizer' in event:
        markdown += "\n## Organizer\n\n"
        organizer = event['organizer']
        markdown += f"- **Name**: {organizer.get('displayName', 'N/A')}\n"
        markdown += f"- **Email**: {organizer.get('email', 'N/A')}\n"
    
    # Handle conferencing data (e.g., Google Meet links)
    if 'conferenceData' in event:
        markdown += "\n## Conference Information\n\n"
        conf_data = event['conferenceData']
        
        if 'entryPoints' in conf_data:
            markdown += "### Entry Points\n\n"
            for entry in conf_data['entryPoints']:
                entry_type = entry.get('entryPointType', 'N/A')
                uri = entry.get('uri', 'N/A')
                markdown += f"- **Type**: {entry_type}\n"
                markdown += f"  **URI**: {uri}\n"
    
    # Add all remaining fields as JSON
    markdown += "\n## All Fields\n\n"
    markdown += "```json\n"
    markdown += json.dumps(event, indent=2)
    markdown += "\n```\n"
    
    return markdown

def main():
    parser = argparse.ArgumentParser(description='Get details for a Google Calendar event.')
    parser.add_argument('--event-id', type=str, default=DEFAULT_EVENT_ID,
                        help=f'The ID of the event to retrieve (default: {DEFAULT_EVENT_ID})')
    parser.add_argument('--calendar-id', type=str, default='primary',
                        help='The calendar ID (default: primary)')
    
    args = parser.parse_args()
    
    print(f"Retrieving details for event: {args.event_id}")
    event = get_event_details(args.event_id, args.calendar_id)
    
    if event:
        markdown = format_event_as_markdown(event)
        print(markdown)
    else:
        print("Failed to retrieve event details.")

if __name__ == '__main__':
    main()