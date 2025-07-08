import pyttsx3
import os

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

def text_to_speech(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                read = file.read()
                return read
        else:
            print("File does not exist.")
            return None

    except FileNotFoundError:
        print("File not found")
        return None

if __name__ == "__main__":
    print("Text-to-Speech File Reader")
    file_path = input("Enter the filename to read: ")

    content = text_to_speech(file_path)

    if content:
        print("Speaking the content now...")
        speak(content)
        print("Done speaking the file contents.")
