import tkinter as tk
from tkinter import messagebox
import json
import os

MODEL_FILE = "memory.json"
model = {}

# -------------------------------
# TEXT PROCESSING
# -------------------------------
def clean_text(text):
    text = text.lower()
    cleaned = ""

    for ch in text:
        if ch.isalnum() or ch.isspace():
            cleaned += ch
        else:
            cleaned += " "

    return cleaned.split()

# -------------------------------
# TRAIN MODEL
# -------------------------------
def train_model(words):
    global model

    for i in range(len(words) - 2):
        key = (words[i], words[i+1])
        next_word = words[i+2]

        if key not in model:
            model[key] = {}

        if next_word not in model[key]:
            model[key][next_word] = 0

        model[key][next_word] += 1

# -------------------------------
# PREDICTION
# -------------------------------
def predict(w1, w2):
    key = (w1, w2)

    if key not in model:
        return []

    data = model[key]
    sorted_words = sorted(data.items(), key=lambda x: x[1], reverse=True)

    return [w for w, _ in sorted_words[:3]]

def fallback(word):
    result = {}

    for key in model:
        if key[0] == word:
            for w in model[key]:
                result[w] = result.get(w, 0) + model[key][w]

    sorted_words = sorted(result.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:3]]

def get_suggestions():
    text = entry.get()
    words = clean_text(text)

    if len(words) < 2:
        output_label.config(text="Type at least 2 words bro")
        return

    w1, w2 = words[-2], words[-1]

    result = predict(w1, w2)

    if not result:
        result = fallback(w2)

    if not result:
        result = ["No suggestion"]

    output_label.config(text=" | ".join(result))

# -------------------------------
# LEARN FUNCTION
# -------------------------------
def learn_text():
    text = entry.get()
    words = clean_text(text)
    train_model(words)
    messagebox.showinfo("Info", "Model updated!")

# -------------------------------
# SAVE / LOAD
# -------------------------------
def save_model():
    temp = {}

    for key in model:
        temp[key[0] + "|" + key[1]] = model[key]

    with open(MODEL_FILE, "w") as f:
        json.dump(temp, f)

def load_model():
    global model

    if not os.path.exists(MODEL_FILE):
        return

    with open(MODEL_FILE, "r") as f:
        temp = json.load(f)

    for key in temp:
        w1, w2 = key.split("|")
        model[(w1, w2)] = temp[key]

# -------------------------------
# INITIAL DATA
# -------------------------------
def load_initial():
    text = """
    i am going to college
    i am feeling happy today
    you are very smart
    you are my friend
    this is a cool project
    """

    words = clean_text(text)
    train_model(words)

# -------------------------------
# GUI SETUP
# -------------------------------
load_model()
load_initial()

root = tk.Tk()
root.title("Text Autocomplete AI")
root.geometry("400x250")

title = tk.Label(root, text="Autocomplete System", font=("Arial", 14))
title.pack(pady=10)

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

predict_btn = tk.Button(btn_frame, text="Get Suggestions", command=get_suggestions)
predict_btn.grid(row=0, column=0, padx=5)

learn_btn = tk.Button(btn_frame, text="Train", command=learn_text)
learn_btn.grid(row=0, column=1, padx=5)

save_btn = tk.Button(btn_frame, text="Save", command=save_model)
save_btn.grid(row=0, column=2, padx=5)

output_label = tk.Label(root, text="Suggestions will appear here", fg="blue")
output_label.pack(pady=20)

root.mainloop()