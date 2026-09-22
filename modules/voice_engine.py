# modules/voice_engine.py

import pyttsx3

def speak(text, rate=150):
    """
    Converts text to speech.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Adjust speed
    engine.say(text)
    engine.runAndWait()