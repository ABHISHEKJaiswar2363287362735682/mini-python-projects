import pyttsx3

def speak(text):
    engine = pyttsx3.init()

    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)

    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.0)

    engine.say(text)
    engine.runAndWait()

if __name__  == "__main__":
    print("Text to speech CLI Converter")
    text = input("Enter the text you want to convert to speech:\n>")
    speak(text)
    print("Done speaking!")

    