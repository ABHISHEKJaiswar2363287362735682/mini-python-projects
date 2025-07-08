import speech_recognition as sr

def listen_and_process():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Please speak now. I am listening...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        save_output(text)
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand what you said.")
    except sr.RequestError:
        print("⚠️ Could not request results. Check your internet connection.")

def save_output(text):
    with open("voice_notes.txt", "a") as file:
        file.write(text + "\n")
    print("📝 Note saved to 'voice_notes.txt'.")

def main():
    listen_and_process()

if __name__ == "__main__":
    main()
