from __future__ import print_function

import datetime
from datetime import timezone,date
import os.path


import httplib2
import flask
import google_auth_oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import polling2, time
import sys
sys.path.append('../electronics/electronics_programs/')
 
on_raspi = True
try:
    import led_pi as ld
    ld.blink(3) # blinks three times on raspi if library imported correctly
except:
    on_raspi = False



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid']

def getGoogleCalendarList():
    """ Get Google Calendar list
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
    Returns:
        A list of Google calendar name and id pairs"""
    page_token = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("ERROR: token.json missing")
        exit(1)

    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    calendar_names_id_pair = {}
    for calendar_list_entry in calendar_list['items']: 
        calendar_names_id_pair[calendar_list_entry['id']] = calendar_list_entry['summary']
    return calendar_names_id_pair

def get_user_info():
    """Send a request to the UserInfo API to retrieve the user's information.
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
    Returns:
        User information as a dict.
    """
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("ERROR: token.json missing")
        exit(1)
    user_info_service = build(
        serviceName='oauth2', version='v2',
        credentials=creds)
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
    except HttpError as e:
        print('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        print("No user id")

@polling2.poll_decorator(step=2, timeout=0)
def getGoogleCalendarEvent(calendarId='primary'):
    """Get all events on the user's calendar of the current day.
    If some events ends later than current time, turn LED on.
    If no events or all events have passed, turn LED off.
    Args:
        credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                    request.
    Returns:
        None.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        print("ERROR: token.json missing")
        exit(1)
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        today = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time())
        tomorrow = today + datetime.timedelta(days=1)
        # utc_today = today.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        # utc_tomorrow = tomorrow.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        utc_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # tom = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'
        utc_tom = datetime.datetime.utcfromtimestamp(tomorrow.timestamp()).strftime('%Y-%m-%dT%H:%M:%SZ')
        print('Getting the upcoming events')
        events_result = service.events().list(calendarId=calendarId, timeMin=utc_now,
                                              timeMax=utc_tom, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            if on_raspi:
                ld.turn_led_pi("off")
            print('No upcoming events found.')
            return
        else:
            isCurrentEvent = False
            for event in events:
                if datetime.datetime.strptime(event["end"]["dateTime"],'%Y-%m-%dT%H:%M:%S%z').timestamp() > datetime.datetime.now().timestamp():
                    isCurrentEvent = True
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(start, event['summary'])
            if on_raspi and isCurrentEvent:
                ld.turn_led_pi("on")
            

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    getGoogleCalendarEvent()