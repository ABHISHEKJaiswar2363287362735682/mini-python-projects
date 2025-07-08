import requests
import pyttsx3
import speech_recognition as sr

NEWS_API_KEY = '32034b7b2d3642ab8364a39663156b53`'

country_map = {
    'india': 'in', 'united states': 'us', 'canada': 'ca', 'japan': 'jp',
    'australia': 'au', 'germany': 'de', 'france': 'fr'
}

engine = pyttsx3.init()

def speak(text):
    print(f"AI: {text}\n")
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
        return text.lower()
    except:
        speak("Sorry, I could not understand.")
        return ""

def get_news(category, country_code):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': country_code,
        'category': category,
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['status'] == 'ok':
        articles = data['articles'][:5]
        for article in articles:
            speak(article['title'])
    else:
        speak("Failed to fetch news.")

def main():
    speak("Say the category of news you want.")
    category = listen()
    speak("Say the country you want news from.")
    country_input = listen()
    country_code = country_map.get(country_input, 'us')
    speak(f"Fetching {category} news from {country_input if country_input in country_map else 'United States'}.")
    get_news(category, country_code)

if __name__ == "__main__":
    main()
