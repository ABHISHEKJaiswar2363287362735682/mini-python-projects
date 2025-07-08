import speech_recognition as sr
import json
import os
from datetime import datetime

VAULT_FILE = "ai_memory_vault.json"  # fixed spelling

def load_vault():
    if not os.path.exists(VAULT_FILE):
        with open(VAULT_FILE, "w") as f:
            json.dump([], f)
    with open(VAULT_FILE, "r") as f:
        return json.load(f)

def save_vault(vault):
    with open(VAULT_FILE, "w") as f:
        json.dump(vault, f, indent=4)

def listen_and_store():  # fixed function name
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)
        print("Start speaking. Say 'stop memory vault' to end.")

        vault = load_vault()

        while True:  # fixed syntax
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

                if "stop memory vault" in text.lower():  # fixed phrase
                    print("Stopping memory vault session.")
                    break

                if ":" in text:
                    tag, content = map(str.strip, text.split(":", 1))
                else:
                    tag = "general"
                    content = text

                memory_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tag": tag.lower(),
                    "content": content
                }
                vault.append(memory_entry)
                save_vault(vault)
                print(f"Saved memory under tag '{tag}': {content}")  # fixed f-string

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError:
                print("Could not request result, check your internet connection.")
                break

def main():
    listen_and_store()

if __name__ == "__main__":
    main()
