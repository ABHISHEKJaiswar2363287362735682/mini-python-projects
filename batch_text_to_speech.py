# batch_text_to_speech.py

import pyttsx3

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print("❌ The specified file was not found. Please check the filename and path.")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    print("📢 Batch Text-to-Speech File Reader")
    file_path = input("Enter the path of the text file you want to convert to speech:\n> ")

    text_content = read_file_content(file_path)

    if text_content:
        print("🔊 Speaking the contents of the file...")
        speak_text(text_content)
        print("✅ Finished speaking the file contents!")
