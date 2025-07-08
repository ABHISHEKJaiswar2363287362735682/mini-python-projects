import qrcode
import pyttsx3
import qrcode.constants

# Initialize TTS engine
engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def generate_qr(data, filename):
    qr = qrcode.QRCode(
        vesion = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H, 
        box_size= 10,
        border = 4
    )
    qr.add_data(data)
    qr.make(fit = True)

    img = qr.make_image(fill_color = "black", back_color = "white")
    img.save(fit = True)
       
    speak(f"QR code has been generated and saved as {filename}")


def main():
    speak("QR Code Generator Loaded.")
    data = input("Enter the data or URL to generate QR code: ")
    filename = input("Enter filename to save (example: myqr.png): ")

    generate_qr(data, filename)
    speak("QR Code generation completed. You can scan it using your phone.")

if __name__ == "__main__":
    main()
