import tkinter as tk
from tkinter import scrolledtext
import re
import requests
import random
import wikipedia

# --- Helper Functions ---

def solve_math_expression(expression):
    try:
        url = "https://api.mathjs.org/v4/"
        payload = {"expr": expression}
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return f"The answer is: {response.json().get('result')}"
        else:
            return "Sorry, I couldn't compute that."
    except Exception as e:
        return f"Error: {e}"

def get_name_meaning(name):
    try:
        # Wikipedia sometimes needs a more specific search
        summary = wikipedia.summary(f"{name} (name)", sentences=2)
        return summary
    except Exception as e:
        return f"Sorry, couldn't find info for '{name}'. Error: {e}"

def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = response.json()
        return f"{data['setup']} ... {data['punchline']}"
    except:
        return "Couldn't fetch a joke right now. Try again later!"

def get_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        data = response.json()
        return data['text']
    except:
        return "Couldn't fetch a fact right now. Try again later!"

# --- Logic Engine ---

def respond(user_input):
    user_input = user_input.lower()

    # Greetings
    if re.search(r'\bhello\b|\bhi\b|\bhey\b', user_input):
        return "Hello! How can I help you?"
    elif re.search(r'\bmorning\b', user_input):
        return "Good morning! Hope your day starts well."
    elif re.search(r'\bafternoon\b', user_input):
        return "Good afternoon! How can I help you?"
    elif re.search(r'\bevening\b', user_input):
        return "Good evening! What can I do for you?"
    elif re.search(r'\bnight\b', user_input):
        return "Good night! Rest well and sweet dreams."

    # Math Calculations
    elif re.search(r'\bsolve\b|\bcalculate\b|\bevaluate\b', user_input):
        match = re.search(r'(solve|calculate|evaluate)\s(.+)', user_input)
        if match:
            expression = match.group(2)
            return solve_math_expression(expression)
        return "Please provide a valid math expression."

    # Name meaning feature
    elif re.search(r'\bmeaning of the name\b', user_input):
        match = re.search(r'meaning of the name (\w+)', user_input)
        if match:
            name = match.group(1).capitalize()
            return get_name_meaning(name)
        return "Please specify the name you'd like to know about."

    # Dictionary API
    elif re.search(r'\bmeaning of ([a-zA-Z]+)', user_input):
        match = re.search(r'meaning of ([a-zA-Z]+)', user_input)
        if match:
            word = match.group(1)
            try:
                response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
                if response.status_code == 200:
                    data = response.json()
                    definition = data[0]['meanings'][0]['definitions'][0]['definition']
                    return f"The meaning of '{word}' is: {definition}"
                return f"Couldn't find the meaning of '{word}'."
            except:
                return "Unable to fetch the meaning right now."

    # OS-related questions
    elif re.search(r'\bwhat is an operating system\b|\bwhat is os\b', user_input):
        return "An operating system (OS) is system software that manages computer hardware and software resources."
    elif re.search(r'\bkernel\b', user_input):
        return "The kernel is the core part of an OS. It manages system resources and hardware interaction."

    # University specific
    elif re.search(r'\bwhat is iba\b|\bsukkur iba\b|\bsibau\b', user_input):
        return "Sukkur IBA University is a prestigious public university in Sindh, Pakistan, known for merit and quality."

    # Personal / Authorship
    elif re.search(r'\bwho (made|created|built) (you|this)\b', user_input):
        return "I was created by Aqsa Ali Raza Jamali, Hafza, and Ishifaque."
    elif re.search(r'\bwho are you\b', user_input):
        return "I'm ChatSimple, a rule-based chatbot built with Python."

    # Fun stuff
    elif re.search(r'\bjoke\b|\btell me a joke\b', user_input):
        return get_joke()
    elif re.search(r'\bfact\b|\bdid you know\b', user_input):
        return get_fact()
    elif re.search(r'\bmeme\b|\bfunny\b', user_input):
        return random.choice([
            "When you study for 5 minutes and check if success has arrived.",
            "Git commit message: 'Fixed stuff.' Reality: I don't know what I did but it's working.",
            "Teacher: 'The exam will be easy.' The exam: Calculate the mass of the sun using a pencil."
        ])

    # Exit
    elif re.search(r'\bbye\b|\bexit\b|\bquit\b', user_input):
        return "Goodbye! Talk to you later!"

    else:
        return "Hmm, I’m not sure how to respond to that. Try asking about Math, OS, or a joke!"

# --- GUI Setup ---

def send_message():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, "You: " + user_input + "\n", 'user')
    
    response = respond(user_input)
    chat_window.insert(tk.END, "Bot: " + response + "\n\n", 'bot')
    
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Smart Chatbot")
root.geometry("550x550")
root.configure(bg="#f0f8ff")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Segoe UI", 10))
chat_window.pack(padx=10, pady=10)
chat_window.tag_config('user', foreground="blue")
chat_window.tag_config('bot', foreground="green")
chat_window.config(state=tk.DISABLED)

entry = tk.Entry(root, width=60, font=("Segoe UI", 10))
entry.pack(pady=5)
entry.bind("<Return>", lambda event: send_message()) # Press Enter to send

send_button = tk.Button(root, text="Send", command=send_message, bg="#4CAF50", fg="white", font=("Segoe UI", 10))
send_button.pack(pady=5)

# Welcome Message
chat_window.config(state=tk.NORMAL)
chat_window.insert(tk.END, "Bot: Hello! I am ChatSimple. Ask me something interesting.\n\n", 'bot')
chat_window.config(state=tk.DISABLED)

root.mainloop()
