# Subtle Reminder Implementation Plan

## Goal
The Subtle Reminder will light up dimly at night if there’s a TODO item on the Google Calendar. Once the TODO item is marked as completed, the light will be turned off.

## Required hardware components
* Variety of jumper wires
* Multicolor LEDs
* 220 OHM resistors 
* Raspberry pi 4
* Breadboard
* 3D printed case for breadboard 

## Required software components

### Google Calendar API
#### Google api with javascript 
https://developers.google.com/calendar/api/quickstart/js#python-3.x
Find the html file in src/templates/googleCalendar.html.

#### Google api with Python
https://developers.google.com/calendar/api/quickstart/python
Find the python file in src/googleCalendar.py
Currently, Google Calendar API request only works when running python app.py directly.

Set up "Webhook" callback receiver for Google Calendar push notification at https://amarantini.github.io/ (hosted by github).

### Webapp
* Read user input (Gmail and password)
* Google account authentication (Reference: https://realpython.com/flask-google-login/)
* Using Python 

### Set up Google Oauth on server
- Use Flow instead of InstalledAppFlow
- Use flask.url_for to save session info when redirectinh
- Set app.config['SERVER_NAME'] to use a different domain for url_for
- Use nip.io to bypass Google's restriction on using private IP address 
