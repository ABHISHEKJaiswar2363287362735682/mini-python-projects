import speech_recognition as sr  # We import the speech recognition module to convert speech to text

def listen_and_save_note():
    recognizer = sr.Recognizer()  # This helps capture and understand your voice
    mic = sr.Microphone()  # This accesses your system microphone

    print("🎤 Please speak now. I am listening...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)  # Helps reduce background noise
        audio = recognizer.listen(source)  # Listens to your speech

    try:
        text = recognizer.recognize_google(audio)  # Uses Google’s free API to convert speech to text
        print(f"✅ You said: {text}")

        with open("voice_notes.txt", "a") as file:  # Opens/creates a text file to save your notes
            file.write(text + "\n")

        print("📝 Note saved to 'voice_notes.txt'.")

    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand what you said.")
    except sr.RequestError:
        print("⚠️ Could not request results. Check your internet connection.")

if __name__ == "__main__":
    listen_and_save_note()
