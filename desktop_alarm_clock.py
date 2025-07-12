import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
import pygame

# Initialize pygame mixer
pygame.mixer.init()

def play_alarm_sound():
    try:
        pygame.mixer.music.load("alarm.mp3")  # Use full path if needed
        pygame.mixer.music.play(loops=0)
    except Exception as e:
        messagebox.showerror("Error", f"Error playing alarm sound: {e}")

def stop_alarm():
    pygame.mixer.music.stop()
    messagebox.showinfo("Alarm", "Alarm Stopped.")

def set_alarm():
    alarm_time = entry.get()
    if not alarm_time:
        messagebox.showerror("Error", "Please enter the time in HH:MM:SS format.")
        return

    def check_alarm():
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            time_label.config(text=f"Current Time: {current_time}")
            if current_time == alarm_time:
                messagebox.showinfo("Alarm", "Time to wake up!")
                play_alarm_sound()
                break
            time.sleep(1)

    threading.Thread(target=check_alarm, daemon=True).start()

# Create main window
root = tk.Tk()
root.title("Alarm Clock")
root.geometry("400x250")

# Label for instructions
label = tk.Label(root, text="Enter the Alarm Time (HH:MM:SS):", font=("Arial", 14))
label.pack(pady=10)

# Entry for alarm time
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=5)

# Set Alarm button
set_button = tk.Button(root, text="Set Alarm", command=set_alarm, font=("Arial", 12), bg="black", fg="white")
set_button.pack(pady=10)

# Stop Alarm button
stop_button = tk.Button(root, text="Stop Alarm", command=stop_alarm, font=("Arial", 12), bg="red", fg="white")
stop_button.pack(pady=5)

# Label for current time
time_label = tk.Label(root, text="Current Time: --:--:--", font=("Arial", 14))
time_label.pack(pady=10)

# Run the GUI loop
root.mainloop()
