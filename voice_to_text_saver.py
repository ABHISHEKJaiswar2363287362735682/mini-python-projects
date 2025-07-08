import speech_recognition as sr 

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak something...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    with open("Saverd voice_taxt.txt", "w", encoding = "utf-8") as file:
        file.write(text)

    print("Txt saved to 'saved_voice_text.txt")

except sr.UnknownValueError:
    print("Sorry, I couldn't understand your voice")

except sr.RequestError as e:
    print("Could not request result from Google Speech recognition service")
