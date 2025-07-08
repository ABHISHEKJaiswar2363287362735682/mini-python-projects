import speech_recognition as sr 
import pyttsx3 
from googletrans import Translator
import json
from datetime import datetime
import os

engine = pyttsx3.init()
translator = Translator()

HISTORY_FILE = "translator_history.json"

def speak(text, lang="en"):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

def save_history(original, translated, src_lang, dest_lang):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
    
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original": original,
        "translated": translated,
        "source_language": src_lang,
        "target_language": dest_lang
    }

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def get_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for your phrase to translate...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand")
        return ""
    except sr.RequestError:
        speak("Check your internet connection")
        return ""

def translate_text(text, dest_lang='hi'):
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text, translated.src
    except Exception as e:
        speak("An error occurred during translation")
        return None, None

def main():
    speak("Welcome to the Voice Translator. Say 'stop translator' to exit.")
    dest_lang = input("Enter target language code (e.g., 'hi' for Hindi, 'fr' for French): ").strip()

    while True:
        text = get_audio()

        if text and "stop translator" in text.lower():
            speak("Stopping the translator. Goodbye!")
            break

        if text:
            speak("Translating your phrase...")
            translated_text, src_lang = translate_text(text, dest_lang)

            if translated_text:
                speak(f"The translated text is: {translated_text}")
                print(f"[{src_lang} -> {dest_lang}] {translated_text}")
                save_history(text, translated_text, src_lang, dest_lang)

if __name__ == "__main__":
    main()
