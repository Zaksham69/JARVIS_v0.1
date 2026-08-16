# 🤖 JARVIS-V0.1

JARVIS-V0.1 is a simple, non-AI, voice-controlled PC assistant built in Python.

It can open applications, call and message contacts, open websites, search Google, search Wikipedia and summarize results, manage contacts, and more.

## ✨ Features
- 🎙️ Voice-controlled commands
* 🚀 Open applications using configurable .exe paths
+ 🌐 Open websites and search Google
- 📖 Wikipedia search with automatic summaries
- 📞 Call contacts through WhatsApp
- 💬 Send WhatsApp messages
- 👤 Add and manage contacts
- 🗃️ Store client information using JSON
- 📝 Store and manage notes
- 🖱️ Coordinate-based automation
- ⚙️ Customizable application and coordinate configuration

## 🛠️ Requirements
- Python
- Working microphone
- Internet connection for speech recognition and Wikipedia
- WhatsApp Desktop for calling and messaging
- Python modules
- pyttsx3
- SpeechRecognition
- PyAutoGUI
- Wikipedia
- PyAudio

Install the required modules before running JARVIS.

## ⚡ Quick Start
**1. Configure [apps.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/apps.json)**

Add the .exe path or Windows Target of the applications you want JARVIS to control.

Application names must be written in ALL CAPS.

Example:

  {
  
      "VSCODE": "C:\\Path\\To\\Code.exe",
      "CHROME": "C:\\Path\\To\\Chrome.exe"
    
  }

To find an application's Target:

Right-click → Properties → Target

If the Target cannot be copied, you can use an image-to-text tool such as ImageToText.info.

Remember to replace \\ with \\\\ in JSON paths.

**2. Configure coords.json**

Some JARVIS features use mouse coordinates.

Add the required X/Y coordinates to [coords.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coords.json).

Example:

{

    "WHATSAPP_SEARCH_BOX": [150, 120],
    "WHATSAPP_FIRST_RESULT": [150, 270],
    "WHATSAPP_CALL_BUTTON": [1775, 70]
    
}

Run [coord_test.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coord_test.py) to check your coordinates.

Coordinates depend on your screen resolution, display scaling, and window layout. You may need to configure them separately on different computers.

If you don't have Minecraft, you can ignore the Minecraft coordinates.

## 🎙️ Using JARVIS

The main program is [main.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/main.py).

JARVIS uses a wake word before commands.

Say:

"Hey Jarvis"

or:

"Jarvis"

before your command.

Examples

Open an application

"Hey Jarvis, open Chrome"

Search Wikipedia

"Hey Jarvis, Wikipedia Albert Einstein"

JARVIS will return a short summary if a Wikipedia page is available.

Call someone

"Hey Jarvis, call Mom"

Send a message

"Hey Jarvis, message Rahul"

Open a website

"Hey Jarvis, open github.com"

## 👤 Contacts

JARVIS can store alternative names for contacts.

For example, if a contact is saved as _Rahul_, but you normally call him _Bhai_, you can say:

"Hey Jarvis, add contact Rahul as Bhai"

You can also use a WhatsApp number instead of the saved contact name.

If JARVIS asks for something that you would rather type, say:

"written"

and enter it using the keyboard.

## 📁 Project Structure

A typical JARVIS installation contains files such as:


- JARVIS-V0.1/
  - ├── [main.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/main.py)
  - ├── [functions.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/functions.py)
  - |── [apps.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/apps.json)
  - ├── [coords.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coords.json)
  - ├── [contacts.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/contacts.json)
  - ├── [clients.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/clients.json)
  - ├── [notes.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/notes.json)
  - └── [coord_test.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coord_test.py)


JSON files are used for configurable data and stored information, while Python files contain the program logic.

## 🔧 Configuration Tips
- Make sure all application paths in [apps.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/apps.json) are correct.
- Run [coord_test.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coord_test.py) after configuring coordinates.
- Make sure WhatsApp Desktop is installed for WhatsApp features.
- Keep your screen resolution and display scaling consistent after configuring coordinates.
- If an application is moved or reinstalled, update its path in [apps.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/apps.json).
- JARVIS requires an internet connection for speech recognition and Wikipedia.

## 🔒 Privacy

JARVIS may store personal information in files such as [clients.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/clients.json), [contacts.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/contacts.json), and [notes.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/notes.json).

Do not upload real client information, personal contact information, passwords, API keys, or other private data to a public GitHub repository.

Use empty or example JSON files when publishing the project.

## 🐛 Troubleshooting
JARVIS doesn't hear me

Check your microphone, Windows microphone permissions, and make sure you are saying the wake word clearly.

An application doesn't open

Check its path in [apps.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/apps.json).

WhatsApp doesn't work correctly

Check that WhatsApp Desktop is installed and verify the relevant coordinates using coord_test.py.

The mouse clicks the wrong place

Reconfigure the coordinates in [coords.json](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coords.json) and test them using [coord_test.py](https://github.com/Zaksham69/JARVIS_v0.1/edit/main/coord_test.py).

## 🚀 What's Next?

JARVIS-V0.1 is the beginning of the project, not the final version.

More features and improvements will be added over time.

## 📄 License

This project is licensed under the MIT License.

## ❤️ Enjoy!

JARVIS-V0.1 — Built in Python.
