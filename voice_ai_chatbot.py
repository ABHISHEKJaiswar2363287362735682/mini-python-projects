import os
import json
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1")

HISTORY_FILE = "voice_chat_history.json"
engine = pyttsx3.init()

def speak(text):
    print(f"AI: {text}\n")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}\n")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your connection.")
        return ""

def save_history(user_text, bot_text):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    entry = {"user": user_text, "bot": bot_text}
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful AI voice assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return "I encountered an error while generating the response."

def main():
    speak("Voice AI assistant loaded. Say 'stop' to exit.")
    while True:
        user_input = listen()
        if "stop" in user_input.lower():
            speak("Goodbye!")
            break
        if user_input:
            speak("Thinking...")
            bot_response = generate_response(user_input)
            speak(bot_response)
            save_history(user_input, bot_response)

if __name__ == "__main__":
    main()
