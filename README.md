# 🤖 JARVIS-V0.1

**JARVIS-V0.1** is a simple, non-AI, voice-controlled PC assistant built with Python.

It can open applications, call and message contacts, open websites, search Google, search Wikipedia and summarize results, manage contacts and clients, organize notes, and automatically configure screen coordinates.

---

## ✨ Features

* 🎙️ Voice-controlled commands
* 🚀 Open applications using `.exe` paths or Windows Target paths
* 🌐 Open websites
* 🔎 Search Google
* 📖 Search Wikipedia and get short summaries
* 📞 Call contacts
* 💬 Send WhatsApp messages
* 👤 Add and manage contacts
* 🗃️ Store and manage client information
* 📝 Create and manage note families
* 🖱️ Automatically detect screen coordinates
* 🌓 Dark and Light theme support
* 🖥️ Resolution-based coordinate scaling
* ⚙️ JSON-based configuration

---

## 🛠️ Requirements

You need:

* Python
* A working microphone
* An internet connection
* WhatsApp Desktop for WhatsApp features

### Python Modules

Install the required modules before running JARVIS:

```bash
pip install pyautogui
```
```
pip install wikipedia
```
```
pip install pyttsx3
```
```
pip install SpeechRecognition
```


You may also need `PyAudio` depending on your system and speech-recognition setup.

---

## 🚀 Getting Started

### 1. Configure `apps.json`

Open `apps.json` and add the applications you want JARVIS to open.

The application names must be written in **ALL CAPS**.

Example:

```json
{
    "CHROME": "C:\\Path\\To\\Chrome.exe",
    "VSCODE": "C:\\Path\\To\\Code.exe"
}
```

To find an application's path:

**Right-click the application → Properties → Target**

Copy the Target path and add it to `apps.json`.

> **Important:** In JSON, Windows backslashes must be escaped. For example, `C:\Program Files\App` becomes `C:\\Program Files\\App`.

---

### 2. Automatic Coordinate Setup

JARVIS can automatically detect the screen coordinates it needs instead of requiring you to manually enter every coordinate.

On the first run, JARVIS will ask:

> **Are you using Dark theme or Light theme on your PC?**

Choose the theme that matches your Windows settings.

JARVIS will then use the corresponding reference images to locate the required UI elements and save their coordinates to `coords.json`.

### ⚠️ Important

**Do not change the order of the entries in `coords.json`.**

The entries correspond to:

```text
image1.png
image2.png
image3.png
...
```

Changing their order may cause JARVIS to assign the wrong coordinate to the wrong UI element.

---

## 🖥️ Screen Resolution

Some coordinates are calculated relative to a **1920×1080 reference resolution**.

This allows JARVIS to scale certain coordinates automatically when running on a different screen resolution.

---

## 🎙️ Using JARVIS

Run [`main.py`](./main.py) to start JARVIS.

Before giving a command, say:

> **"Hey Jarvis"**

or simply:

> **"Jarvis"**

### Examples

**Open an application**

> "Hey Jarvis, open Chrome"

**Open a website**

> "Hey Jarvis, open github.com"

**Search Google**

> "Hey Jarvis, search Google Python"

**Search Wikipedia**

> "Hey Jarvis, Wikipedia Albert Einstein"

JARVIS will provide a short summary if the requested topic has a Wikipedia page.

**Call a contact**

> "Hey Jarvis, call Mom"

**Send a message**

> "Hey Jarvis, message Rahul"

---

## 👤 Contacts

JARVIS can save alternative names for contacts.

For example:

> "Hey Jarvis, add contact Rahul as Bhai"

You can then use:

> "Hey Jarvis, call Bhai"

You can also provide a WhatsApp number instead of a saved contact name.

---

## 🗃️ Client Management

JARVIS can store client information in `clients.json`.

The default client information includes:

* Email
* Phone
* WhatsApp
* Notes

The client system uses JSON so the stored information can be easily accessed and modified.

---

## 📝 Notes

JARVIS supports **note families** for organizing notes.

For example:

> "Hey Jarvis, add note family Work"

You can then add notes to that family and retrieve them later.

Notes are stored in `notes.json`.

---

## 📁 Project Structure

```text
JARVIS-V0.1/
│
├── main.py
├── functions.py
├── apps.json
├── coords.json
├── contacts.json
├── clients.json
├── notes.json
├── coord_test.py
│
└── images/
    ├── dark/
    └── light/
```

---

## 🔧 Tips

* Make sure the paths in `apps.json` are correct.
* Do not change the order of `coords.json`.
* Make sure the reference images match your selected theme.
* Keep WhatsApp Desktop installed for WhatsApp features.
* If an application is moved or reinstalled, update its path in `apps.json`.
* If an application's interface changes significantly, its reference image may need to be replaced.
* JARVIS needs an internet connection for features such as Wikipedia and online speech recognition.

---

## 🔒 Privacy

JARVIS may store personal information in files such as:

* `contacts.json`
* `clients.json`
* `notes.json`

**Do not upload real personal or client information to a public GitHub repository.**

Use example or empty JSON files when publishing your project.

If you use the password functionality, only store a **password hash**, never the actual password.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ❤️ Enjoy!

**JARVIS-V0.1 — A simple voice-controlled PC assistant built with Python.**
