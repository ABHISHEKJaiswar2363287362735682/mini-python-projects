import speech_recognition as sr
import pyttsx3
import wikipedia

engine = pyttsx3.init()

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for your question...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    
    except sr.RequestError:
        speak("Check your internet connection.")
        return ""
    
def fetch_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    
    except wikipedia.DisambiguationError as e:
        speak("Your query was too broad, please be specific.")
        return None

    except wikipedia.PageError:
        speak("No page found for your query.")
        return None
    
    except Exception as e:
        speak("An error occurred while fetching information.")
        return None
    
def main():
    speak("Welcome to the Voice Wikipedia Assistant. Say 'stop assistant' to exit.")

    while True:
        command = get_audio()

        if "stop assistant" in command:
            speak("Stopping the assistant. Goodbye!")
            break

        if command:
            speak("Searching Wikipedia...")
            summary = fetch_wikipedia_summary(command)

            if summary:
                speak("According to Wikipedia, " + summary)

if __name__ == "__main__":
    main()
