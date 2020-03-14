This is a simple Voice Assistant program
Plan to use google's gTTS engine.
Programe will take input from computer's own microphone.
User can add calender events using google's calender API.
Application can extract data from voice.
Application can set events to a specific date in the calender.
Program can replay to with the saved calender event etc.
User can wake the assistant using voice trigger.

Dependancies:
    SpeechRecognition: pip install SpeechRecognition
    Google Text to Speech: pip install gTTS
    playsound: pip install playsound
    pyaudio: download appropriate (python version cpXX, windows bit 32/64) .whl file from
             https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
             pip install C:\Users\maity\Downloads\PyAudio-0.2.11-cp37-cp37m-win_amd64.whl
    Google calender API: go to https://developers.google.com/calendar/quickstart/python?authuser=3
                         press enable the google calender api
                         download the credentials json file to the script location
                         install the python package using,
                         pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    