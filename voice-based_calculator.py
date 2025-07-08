import speech_recognition as sr
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for your calculation...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand")
        return ""
    except sr.RequestError:
        speak("Check your internet connection")
        return ""

def parse_and_calculate(command):
    words = command.replace("by", "").split()
    words = [w.replace(",", "") for w in words]

    operators = {
        "plus": "+",
        "add": "+",
        "+": "+",
        "minus": "-",
        "subtract": "-",
        "-": "-",
        "times": "*",
        "multiply": "*",
        "*": "*",
        "x": "*",               # <-- Added support for 'x'
        "divided": "/",
        "divide": "/",
        "over": "/",
        "/": "/"
    }

    for i, word in enumerate(words):
        if word in operators:
            try:
                num1 = float(words[i - 1])
                num2 = float(words[i + 1])
                op = operators[word]

                if op == '+':
                    result = num1 + num2
                elif op == '-':
                    result = num1 - num2
                elif op == '*':
                    result = num1 * num2
                elif op == '/':
                    if num2 == 0:
                        speak("Division by zero is not allowed.")
                        return None
                    result = num1 / num2
                return result
            except:
                speak("Could not parse numbers. Please try again.")
                return None

    speak("No valid operation found.")
    return None

def main():
    speak("Welcome to the Voice Calculator. Say 'stop calculator' to exit.")
    while True:
        command = get_audio()
        if "stop calculator" in command:
            speak("Stopping voice calculator. Goodbye!")
            break
        if command:
            result = parse_and_calculate(command)
            if result is not None:
                speak(f"The result is {result}")

if __name__ == "__main__":
    main()
