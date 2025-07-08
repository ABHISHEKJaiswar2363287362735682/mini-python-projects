import tkinter as tk

def process_input():
    user_input = entry.get()
    reversed_text = user_input[::-1]
    result_label.config(text=f"Reversed: {reversed_text}")

root = tk.Tk()
root.title("Simple Frontend App")

entry = tk.Entry(root, width=30)
entry.pack(pady=10)

submit_button = tk.Button(root, text="Submit", command=process_input)
submit_button.pack(pady=5)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()
