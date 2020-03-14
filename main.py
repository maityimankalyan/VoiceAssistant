# google calendar API imports
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# my imports
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS  # needs internet to run in realtime
# import pyttsx3  # offline text to speach
import pytz
import subprocess
import requests
import json


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','july', 'august', 'september','october', 'november', 'december']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_EXTENTIONS = ['rd', 'th', 'st', 'nd']

LOC_API_KEY = 'dee0ca070841172d3a2561dab09a82e7'  # get location API key from https://ipstack.com/signup/free
WEATHER_API_KEY = '432d67ca3917cd8f22bb2bcb977c797e'  # get weather API key from https://ipstack.com/quickstart


def speak(text):
    """takes a text and speak it out using google text to speach API"""
    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()
    tts = gTTS(text=text, lang='en')
    filename = 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename, True)
    os.remove(filename)


def get_audio():
    """get the oudio input from the mic of the device"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ''

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print('Exception: {}'.format(e))
    return said.lower()


def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):
    """Call the google Calendar API for user data"""
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=date.isoformat(),
        timeMax=end_date.isoformat(),
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak("No upcoming events for you, eman.")
    else:
        speak(f"eman, you have {len(events)} events on the day.")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split('T')[1].split('+')[0])

            if int(start_time.split(':')[0]) < 12:
                start_time = start_time + ' AM'
            else:
                start_time = str(int(start_time.split(':')[0]) - 12) + start_time.split(':')[1]
                start_time = start_time + ' PM'

            speak("at {} {}".format(start_time, event['summary']))


def get_date(text):
    """gets google Calender data using API"""
    text = text.lower()
    today = datetime.date.today()
    if text.count('today') > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS: month = MONTHS.index(word) + 1
        elif word in DAYS: day_of_week = DAYS.index(word)
        elif word.isdigit(): day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try: day = int(word[:found])
                    except: pass

    if month < today.month and month != -1: year = year + 1
    if day < today.day and month == -1 and day != -1: month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1: dif += 7

        return today + datetime.timedelta(dif)

    if month == -1 or day == -1: return None  # if fail to parse the date

    return datetime.date(month=month, day=day, year=year)


def note(text):
    """saves the note in notepad.exe"""
    date = datetime.datetime.now()
    file_name = 'notes' + '/' + str(date).replace(':', '_') + '_note.txt'
    with open(file_name, 'w') as f:
        f.write(text)

    subprocess.Popen(['notepad.exe', file_name])


def get_location():
    """get the current location using ipstack API"""
    send_url = "http://api.ipstack.com/check?access_key=" + LOC_API_KEY
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    # latitude = geo_json['latitude']
    # longitude = geo_json['longitude']
    city = geo_json['city']
    print('Current location: ', city)
    return city


def get_weather_report(city):
    """gets the current weather report of the city using openweathermap API"""
    report = ''
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + WEATHER_API_KEY + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        temperature = int(current_temperature) - 273
        report = 'currently in {} temperature is {} degree celsius. humidity is {} %. atmospheric pressure is {} hectopascal. and mostly {}'.format(
            city, temperature, current_humidiy, current_humidiy, weather_description)
        print(report)
    else:
        report = city + ' Not Found!'
        print(report)
    return report


# process starts here
SERVICE = authenticate_google()
WAKE = 'hello'
print('== Start ==')
while True:
    print('Listening...')  # always listenling
    text = get_audio()

    if text.count(WAKE) > 0:  # triggers only for the key word, 'hello'
        speak("I am ready")
        text = get_audio()
        # key words for calendar events search
        CALENDER_STRS = ['what do', 'what do i', 'what do i have', 'do i', 'do i have', 'do i have plans', 'am i busy']
        for phrase in CALENDER_STRS:
            if phrase in text:
                date = get_date(text)
                if date: get_events(date, SERVICE)
                else: speak("I did not get you.")
                break  # not to repeat the step if another key word match found for the same
        # keys words for taking notes
        NOTE_STRS = ['note', 'make a note', 'write', 'write it', 'write it down', 'remember', 'remember it']
        for phrase in NOTE_STRS:
            if phrase in text:
                speak("yes, tell me, eman.")
                note_text = get_audio()
                note(note_text)
                speak("I have it in notepad.")
                break
        # key words for for weather report
        WEATHER_STRS = ['weather', 'temperature', 'climate', 'rain', 'umbrella']
        for phrase in WEATHER_STRS:
            if phrase in text:
                city_name = get_location()
                weather_report = get_weather_report(city_name)
                speak(weather_report)
                break
        # key words for thank you
        THANK_STRS = ['thanks', 'thank', 'thank you']
        for phrase in THANK_STRS:
            speak('you are welcome, eman.')
            break
