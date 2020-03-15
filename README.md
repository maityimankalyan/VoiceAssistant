This is a simple Voice Assistant program. Used google's gTTS engine for text to speach convertion (Need internet connection for that). It takes input from computer's own microphone. User can add, ask already existing calender events using google's calender API. Application can extract data in text from voice. Application can set events to a specific date in the calender. User can wake the assistant using voice trigger (hello).

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
             
    User need to approve google Calender API from https://www.googleapis.com/auth/calendar.readonly
    
    For location data get API key from https://ipstack.com/signup/free
    
    For Weather API key use https://ipstack.com/quickstart
    
Currently supported voice commands are,

Take a note  >>  saves what ever user says in notepad

What do i have on March 15th (any day)  >>  get google calender data and say it to user

How is the weather?  >>  says current location's weather report

Thank you  >>  replay with 'you are welcome'
