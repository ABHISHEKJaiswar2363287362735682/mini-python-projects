import speech_recognition as sr
import pyttsx3
import os

# Initialize TTS engine
engine = pyttsx3.init()

def speak_response(text):
    """Speaks the given text aloud using TTS."""
    print("🤖 Speaking:", text)
    engine.say(text)
    engine.runAndWait()

def listen_and_process():
    """Listens to your voice and converts it to text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Please say the file name you want to open (e.g., notes.txt)")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand your voice.")
        speak_response("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("⚠️ Could not request results. Check your internet connection.")
        speak_response("There was a network error.")
        return ""

def open_and_read_file(filename):
    """Opens and reads the file if it exists, else informs user."""
    if os.path.exists(filename):
        speak_response(f"Opening {filename}")
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"📄 Content of {filename}:\n{content}")
            speak_response(content[:200])  # Speak only first 200 chars to avoid overflow
    else:
        msg = f"The file {filename} does not exist in the folder."
        print(msg)
        speak_response(msg)

def clean_filename(text):
    cleaned = text.lower()
     
    cleaned = text.lower()
    replacements = {
        " dot ": ".",
        " point ": ".",
        " period ": ".",
        " underscore ": "_",
        " under score ": "_",
        " dash ": "-",
        " hyphen ": "-",
        " slash ": "/",
        " forward slash ": "/",
        " backslash ": "\\",
        " colon ": ":",
        " apostrophe ": "'",
        " comma ": ",",
        " space ": " ",
        " new line ": "\n"
    }
    for spoken, symbol in replacements.items():
        cleaned = cleaned.replace(spoken, symbol)
    
    cleaned = cleaned.replace(" ", "") 
    return cleaned.strip()

def main():
    filename = listen_and_process()
    if filename:
        
        filename_clean = clean_filename(filename)
        open_and_read_file(filename_clean)

if __name__ == "__main__":
    main()
