import speech_recognition as sr 
import pyttsx3
import webbrowser
import datetime

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Adjusting for noise...")

        recognizer.adjust_for_ambient_noise(source)
        print("Listening for command...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"You said {text}")
        return text
    
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    
    except sr.RequestError as e:
        print(f"API Error: {e}")
        return ""
    
def execute_command(command):
    if "open youtube" in command:
        speak("opening youtube")
        webbrowser.open("https://www.youtube.com")
    
    elif "what is the time" in command or "tell me the time" in command:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        speak(f"The current time is {time_str}")
    elif "hello" in command:
        speak("Hello, how can I assist you today?")
    elif "exit" in command or "quit" in command:
        speak("Goodbye")
        return False
    else:
        speak("Sorry,  I did not understand the command")
        return True
    
if __name__ == "__main__":
    speak("Voice commander Executer is Ready, Please speak your command.")

    while True:
        command = listen_and_transcribe()
        if command.strip()!= "":
            continue_running = execute_command(command)

            if not continue_running:
                break