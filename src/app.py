# Python standard libraries
import json
import os
import sqlite3
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

import sys
sys.path.append('../electronics/electronics_programs/')
 
on_raspi = True
try:
    import led_pi as ld
    ld.blink(3) # blinks three times on raspi if library imported correctly
except:
    on_raspi = False


# Third-party libraries
import flask
from flask import Flask, redirect, request, url_for, render_template, send_from_directory
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleCalendar import getGoogleCalendarEvent, getGoogleCalendarList, get_user_info

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
        # 'https://mail.google.com/',
        # 'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid']

# Flask app setup



app = Flask(__name__, static_url_path='', static_folder='../client/dist')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# global variable for ip address of pi on private network 
# change this address to whatever ip the pi is assigned on specific network 
if on_raspi:
    global_ip = "192.168.0.27" + ".nip.io:5000"
    global_app_ip = "192.168.0.27.nip.io"
    app.config['SERVER_NAME'] = global_ip


def credentials_to_dict(credentials):
  """Convert credentials to dictionary"""
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


@app.route("/")
def index():
    return send_from_directory('../client/dist', 'index.html')

@app.route("/login")
def login():
    """Login using Google Oauth
    Args:
        None
    Returns:
        Redirect to authorization page"""

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", scopes=SCOPES)

    flow.redirect_uri =  flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
      # Enable offline access so that you can refresh an access token without
      # re-prompting the user for permission. Recommended for web server apps.
      access_type='offline',prompt='consent',
      # Enable incremental authorization. Recommended as a best practice.
      include_granted_scopes='true')

  # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route("/user")
def getUserInfo():
    """Get user information from Google.
    Args:
        Credentials
    Returns:
        User information on Google account
    """
    user_info = get_user_info()
    print(user_info)
    return user_info

@app.route("/select-calendar", methods=["POST"])
def selectCalendar():
    """ Get the calendar ID from the request.
    Check the events from the calendar and modify LED state.
    Args:
        calendarId - Google Calendar ID
    Returns:
        None"""
    calendarId = request.json.get('calendarId')
    getGoogleCalendarEvent(calendarId)

@app.route("/calendar-list")
def listCalendar():
    """List user's calendar
    Args:
        Credentials
    Returns:
        A list of Google calendar name and id pairs"""
    return getGoogleCalendarList()


@app.route('/oauth2callback')
def oauth2callback():
    """Callback function for login
    Store credentials to local device at token.json
    Args:
        None
    Returns:
        Redirect to index page"""
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "credentials.json", scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url

    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)
    #   flask.session['credentials'] = credentials
    with open('token.json', 'w') as token:
        json.dump(flask.session['credentials'],token)

    return flask.redirect(flask.url_for("index"))



# Max's edits, setup testing page for interacting with led over site
@app.route("/testpage")
def testpage():
    return render_template('test_page.html')


@app.route("/turnledon")
def turnledon():
    """Test: turn led on"""
    if on_raspi:
        ld.turn_led_pi("on")
    else:
        print("not connected to pi")
        pass
    return render_template('test_page.html')

@app.route("/turnledoff")
def turnledoff():
    """Test: turn led off"""
    if on_raspi:
        ld.turn_led_pi("off")
    else:
        print("not connected to pi")
        pass
    return render_template('test_page.html')

@app.route("/breatheled")
def breatheled():
    """Test: breath led"""
    if on_raspi:
        ld.breathe(30)
    else:
        print("not connected to pi")
        pass
    return render_template('test_page.html')



if __name__ == "__main__":
    if on_raspi:
         app.run(global_app_ip,ssl_context="adhoc")
    else:
        app.run(ssl_context="adhoc")

