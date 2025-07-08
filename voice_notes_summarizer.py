import speech_recognition as sr
import pyttsx3
from datetime import datetime
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env automatically
load_dotenv()

# Initialize TTS
engine = pyttsx3.init()

# Initialize OpenRouter client via OpenAI compatible SDK
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    print("AI: OpenRouter API key is missing. Please set it in your .env file as OPENROUTER_API_KEY.")
    exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

HISTORY_FILE = "summaries.json"

def speak(text):
    print(f"\nAI: {text}\n")
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening to your notes...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"\nYou said: {text}\n")
        return text
    
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""

    except sr.RequestError:
        speak("Check your internet connection.")
        return ""
    
def summarize_note(note):
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes notes into 3-5 clear bullet points."},
                {"role": "user", "content": f"Please summarize this note:\n\n{note}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary
    
    except Exception as e:
        speak("An error occurred while summarizing the note.")
        print(e)
        return None
    
def save_memory(original, summary):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
    
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_note": original,
        "summary": summary
    }

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def main():
    speak("Welcome to the Voice Notes Summarizer using OpenRouter. Say 'stop' to exit.")

    while True:
        note = get_audio()

        if "stop" in note.lower():
            speak("Stopping the summarizer. Goodbye!")
            break

        if note:
            speak("Summarizing your note...")
            summary = summarize_note(note)

            if summary:
                speak("Here is your summary:")
                speak(summary)
                save_memory(note, summary)

if __name__ == "__main__":
    main()
