import PyPDF2
import faiss
import numpy as np
import tiktoken
import os
import json
import pyttsx3
import speech_recognition as sr
from openai import OpenAI

engine = pyttsx3.init()
os.environ["OPENAI_API_KEY"] = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1")

HISTORY_FILE = "qa_history.json"

def load_pdf_chunks(file_path, chunk_size=500):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def embed_chunks(chunks):
    embeddings = []
    enc = tiktoken.get_encoding("cl100k_base")
    for chunk in chunks:
        tokens = enc.encode(chunk)
        vector = np.array([len(tokens)] * 384).astype('float32')
        embeddings.append(vector)
    return np.vstack(embeddings)

def speak(text):
    print(f"\nAI: {text}\n")
    engine.say(text)
    engine.runAndWait()

def get_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Listening for your question...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"\n🗣️ You said: {text}\n")
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        speak("Check your internet connection.")
        return ""

def save_history(question, answer):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    entry = {
        "question": question,
        "answer": answer
    }
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_answer(context, question):
    try:
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer clearly:"
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a PDF assistant that answers user questions accurately using the provided context."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        speak("An error occurred while generating the answer.")
        print(e)
        return "Error generating answer."

def main():
    speak("Loading your PDF...")
    chunks = load_pdf_chunks("document.pdf")
    embeddings = embed_chunks(chunks)

    index = faiss.IndexFlatL2(384)
    index.add(embeddings)

    speak("PDF loaded. You can now ask your questions. Say 'stop' to exit.")

    while True:
        question = get_audio()
        if "stop" in question.lower():
            speak("Exiting the PDF assistant. Goodbye!")
            break
        if question:
            enc = tiktoken.get_encoding("cl100k_base")
            tokens = enc.encode(question)
            query_vector = np.array([len(tokens)] * 384).astype('float32').reshape(1, -1)

            distances, indices = index.search(query_vector, 1)
            context = chunks[indices[0][0]]

            speak("Thinking and finding the best answer...")
            answer = generate_answer(context, question)

            speak("Here is the answer:")
            speak(answer)

            save_history(question, answer)

if __name__ == "__main__":
    main()
