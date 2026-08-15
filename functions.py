
import pyttsx3
import speech_recognition as sr
import pyautogui
import time as _Time
import subprocess
import json
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

SCRIPT_DIR = Path(__file__).parent.resolve()

APPS_FILE = SCRIPT_DIR / "apps.json"
CONTACTS_FILE = SCRIPT_DIR / "contacts.json"
COORDS_FILE = SCRIPT_DIR / "coords.json"
CLIENTS_FILE = SCRIPT_DIR / "clients.json"
NOTES_FILE = SCRIPT_DIR / "notes.json"


# =========================================================
# LOAD JSON FILES
# =========================================================

def load_json(file_path, default=None):
    if default is None:
        default = {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return default

    except json.JSONDecodeError:
        print(f"Invalid JSON file: {file_path}")
        return default


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


APPS = load_json(APPS_FILE)
CONTACTS = load_json(CONTACTS_FILE)
COORDS = load_json(COORDS_FILE)


# =========================================================
# ENGINE
# =========================================================

engine = pyttsx3.init()

WAKE_WORDS = (
    "hey jarvis",
    "jarvis",
    "hey jervis",
    "hey jarviss",
    "ok jarvis"
)


# =========================================================
# LISTEN
# =========================================================

def listen():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source)

            try:
                cmd = recognizer.recognize_google(audio).lower().strip()

                print("You said:", cmd)

                return cmd

            except sr.UnknownValueError:
                print("Could not understand audio")
                return None

            except sr.RequestError as e:
                print("Speech recognition error:", e)
                return None

    except OSError:
        print("Microphone not found")
        return None


# =========================================================
# SPEAK
# =========================================================

def say(text):
    engine.say(str(text))
    engine.runAndWait()


def sayywrite(text):
    print(text)
    say(text)


# =========================================================
# MOUSE
# =========================================================

def move(x, y):
    pyautogui.moveTo(x, y)


def write(text):
    pyautogui.write(str(text), interval=0.05)


def home_screen():
    pyautogui.hotkey("win", "m")


# =========================================================
# CALL
# =========================================================

def call(name):
    sayywrite(f"Calling {name}")

    home_screen()

    try:
        subprocess.Popen([
            "explorer.exe",
            f"shell:AppsFolder\\{APPS['WHATSAPP']}"
        ])

    except KeyError:
        sayywrite("WhatsApp is not configured in apps.json.")
        return

    _Time.sleep(2)

    move(*COORDS["WHATSAPP_SEARCH_BOX"])
    pyautogui.click()

    write(name)

    _Time.sleep(1)

    move(*COORDS["WHATSAPP_FIRST_RESULT"])
    pyautogui.click()

    move(*COORDS["WHATSAPP_CALL_BUTTON"])
    pyautogui.click()


# =========================================================
# CLIENT JSON
# =========================================================

def load_clients():
    return load_json(CLIENTS_FILE, {})


def save_clients(clients):
    save_json(CLIENTS_FILE, clients)

# =========================================================
# NOTES JSON
# =========================================================
def load_notes():
    return load_json(NOTES_FILE, {})

def save_notes(notes):
    save_json(NOTES_FILE, notes)


# =========================================================
# FIELD ASK
# =========================================================

def ask_field(ask):
    print(ask + ": ")
    say(ask)

    field = listen()

    if field is None:
        sayywrite(f"I didn't catch the {ask.lower()}.")
        return None

    # Allow the user to type instead of speaking.
    #
    # Example:
    # Voice says "written"
    # Then use whatever was typed in the console.

    if field == "written" or "written" in field:
        wfield = input(ask + ": ").strip()

        if not wfield:
            return None

        field = wfield

    return field.strip()

def print_noteFamily(noteFamily):
    notes = load_notes()
    print(noteFamily,'-')
    for i in range(len(notes[noteFamily])):
        print("      ",i+1,". ", notes[noteFamily][i],"\n")

def return_noteFamily(noteFamily):
    notes = load_notes()
    for i in range(len(notes[noteFamily])):
        return f"      {i+1}. {notes[noteFamily][i]}\n"