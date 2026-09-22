import os
import time
import pyttsx3
import speech_recognition as sr
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize Hugging Face client
client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=HF_TOKEN
)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Memory of past interactions
history = []

# Log file
LOG_FILE = "conversations.txt"

# Learning style (default is verbal)
learning_style = "verbal"

# Speak text aloud
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("?? Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "I couldn't understand, please try again."
    except sr.RequestError as e:
        return f"Speech recognition error: {e}"

# Generate a simple visual aid using matplotlib
def generate_visual(concept, text_description):
    try:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis("off")
        ax.text(0.5, 0.5, f"{concept}\n\n{text_description[:300]}...", 
                wrap=True, ha='center', va='center', fontsize=12)
        plt.title(f"Visual Aid: {concept}")
        plt.tight_layout()
        plt.savefig("visual.png")
        print("??? Visual saved as visual.png")
    except Exception as e:
        print(f"Failed to generate visual: {e}")

# Explain concept based on learning style
def explain_concept(concept):
    global history
    base_prompt = (
        f"Explain the concept of '{concept}' in a simple, clear way for a student "
        f"who learns best in a {learning_style} style."
    )
    messages = history + [{"role": "user", "content": base_prompt}]

    try:
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        reply = response.choices[0].message.content.strip()

        # If reply is too short or generic, try rephrased prompt
        if len(reply) < 40 or "I don't know" in reply.lower():
            fallback_prompt = (
                f"Please teach me about '{concept}' like I'm a beginner. "
                f"Use {learning_style} explanation if possible."
            )
            messages.append({"role": "user", "content": fallback_prompt})
            response = client.chat_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )
            reply = response.choices[0].message.content.strip()

        # Save interaction
        history.append({"role": "user", "content": base_prompt})
        history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"?? Error: {e}"


# Ask user for preferred learning style
def select_learning_style():
    global learning_style
    print("\n?? Select your learning style:")
    print("1. Visual ???")
    print("2. Auditory ??")
    print("3. Verbal ??")
    choice = input("Enter 1, 2 or 3: ").strip()
    if choice == "1":
        learning_style = "visual"
    elif choice == "2":
        learning_style = "auditory"
    else:
        learning_style = "verbal"
    print(f"\n? Learning style set to: {learning_style.capitalize()}")

# Main loop
if __name__ == "__main__":
    print("?? NeuroLearn Assistant Started (say 'exit' to quit)\n")
    select_learning_style()

    while True:
        speak("Please say the concept you want me to explain.")
        concept = listen().lower()

        if "exit" in concept:
            speak("Goodbye!")
            break

        print(f"\n? You asked: {concept}")
        response = explain_concept(concept)
        print(f"\n?? Explanation:\n{response}\n")

        if learning_style in ["auditory", "verbal"]:
            speak(response)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n---\n?? User: {concept}\n?? Bot: {response}\n")
