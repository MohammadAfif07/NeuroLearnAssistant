import pyttsx3
import speech_recognition as sr

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print(f"🗣️ Bot: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except sr.RequestError:
        return "Speech recognition service error."
