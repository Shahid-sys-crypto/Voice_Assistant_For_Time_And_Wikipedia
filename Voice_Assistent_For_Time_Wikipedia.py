from logging import exception

import speech_recognition as sr
from datetime import datetime
import pyttsx3
import wikipedia
import sys

engine=pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def get_time_now():
    now=datetime.now().strftime("%I:%M %p")
    speak(now)
    print(f"current time is {now}")

def search_wikipedia(query):
    try:
        results=wikipedia.summary(query,sentences=2)
        speak(results)
        print(results)
    except wikipedia.exceptions.DisambiguationError:
        speak("please give me correct specification")
        print("please give me correct specification")
    except wikipedia.exceptions.PageError:
        speak("no page found")
        print("no page found")
def recognize_speech():
    recognizer=sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio=recognizer.listen(source)
        text=recognizer.recognize_google(audio)
        print(f"user said :{text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Sorry, I cannot understand")
        speak("Sorry, I cannot understand")
        return None
    except sr.RequestError:
        print("no internet")
        speak("no internet")
        return None
    except exception:
        speak("Sorry, I cannot understand")
        return None
def process_command(command):
    if not command:
        return
    if "time" in command:
        get_time_now()
    elif "wikipedia" in command:
        query=command.replace("wikipedia","").strip()
        if query:
            search_wikipedia(query)
        else:
            speak("what do you want me to tell")
            query=recognize_speech()
            if query:
                search_wikipedia(query)
    elif "exit" in command or "stop" in command:
        speak("exiting now")
        sys.exit()
    else:
        speak("please say clearly i cant understand")

def main():
    speak("welcome to voice assistant how can i help you")
    while True:
        command=recognize_speech()
        if command:
            process_command(command)

if __name__=="__main__":
    main()
