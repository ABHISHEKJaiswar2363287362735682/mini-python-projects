import os
import json
import pyttsx3
import speech_recognition as sr
import requests
from openai import OpenAI

# Initialize TTS
engine = pyttsx3.init()

# Securely load API keys (recommended to move to .env in production)
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(base_url="https://openrouter.ai/api/v1")

HISTORY_FILE = "weather_voice_history.json"

WEATHER_API_KEY = "e46f6f30d8f9e72516a566ee10537bbd"

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You: {text}\n")
        return text

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand.")
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

    entry = {
        "user": user_text,
        "bot": bot_text
    }

    history.append(entry)

    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return "I couldn't find the weather for that location."

        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_info = (
            f"The weather in {city} is currently {weather_desc} with a temperature of {temp}°C, "
            f"humidity of {humidity}%, and wind speed of {wind_speed} meters per second."
        )
        return weather_info

    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Sorry, I encountered an error retrieving the weather."

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return "I encountered an error while generating the response."

def main():
    speak("Weather Voice Assistant loaded. Say 'stop' to exit.")

    while True:
        user_input = listen()

        if "stop" in user_input.lower():
            speak("Goodbye!")
            break

        if "weather" in user_input.lower():
            speak("Which city would you like the weather for?")
            city = listen()
            if city:
                weather_info = get_weather(city)
                speak(weather_info)
                save_history(user_input, weather_info)
        else:
            speak("Thinking...")
            bot_response = generate_response(user_input)
            speak(bot_response)
            save_history(user_input, bot_response)

if __name__ == "__main__":
    main()
