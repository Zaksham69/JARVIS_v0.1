  _____  ______          _____    _______ _    _ _____  _____    ______ _____ _____   _____ _______ 
 |  __ \|  ____|   /\   |  __ \  |__   __| |  | |_   _|/ ____|  |  ____|_   _|  __ \ / ____|__   __|
 | |__) | |__     /  \  | |  | |    | |  | |__| | | | | (___    | |__    | | | |__) | (___    | |   
 |  _  /|  __|   / /\ \ | |  | |    | |  |  __  | | |  \___ \   |  __|   | | |  _  / \___ \   | |   
 | | \ \| |____ / ____ \| |__| |    | |  | |  | |_| |_ ____) |  | |     _| |_| | \ \ ____) |  | |   
 |_|  \_\______/_/    \_\_____/     |_|  |_|  |_|_____|_____/   |_|    |_____|_|  \_\_____/   |_|   
                                                                                                   
                                                                                                   
##JARVIS v0.1

A simple, non-AI, voice-controlled PC assistant built in Python.

##Quick Start

1.Install the required Python modules.

2.Configure apps.json.

3.Configure coords.json.

4.Install WhatsApp Desktop.

##Run JARVIS.

Say "Hey Jarvis" or "Jarvis" before every command.

That's it! 🎉

Requirements

JARVIS uses:

pyttsx3

SpeechRecognition

PyAutoGUI

Wikipedia

PyAudio


A working microphone is also required.


Note: Speech recognition and Wikipedia require an internet connection.


##Configuration

#apps.json


Open apps.json and enter the .exe path or Windows Target of each application next to its name. App names must be written in ALL CAPS.

Example:

{

    "VSCODE": "C:\\Path\\To\\Code.exe",
    
    "CHROME": "C:\\Path\\To\\Chrome.exe"
    
}

To find an application's Target, right-click its shortcut → Properties → Target.

If the Target cannot be copied, you can take a screenshot and use an image-to-text tool such as ImageToText.info to extract it.

Remember that Windows paths in JSON require \\ instead of \.

If an application is moved or reinstalled, its path may need to be updated.

#coords.json

Some JARVIS features use mouse coordinates. Enter the required X and Y coordinates in coords.json.

Run coord_test.py to check your coordinates before using JARVIS.

Coordinates depend on your screen resolution, display scaling, and window layout, so they may need to be configured separately on different computers.

If you don't have Minecraft installed, you can ignore the Minecraft coordinates.

#WhatsApp

Make sure WhatsApp Desktop is installed. JARVIS uses the desktop application for WhatsApp features such as calling and messaging.

##Commands

JARVIS requires a wake word before commands.

#Example:

"Hey Jarvis, open Chrome"

or:

"Jarvis, what is the time?"

Wikipedia

Ask JARVIS to search Wikipedia:

"Hey Jarvis, Wikipedia Albert Einstein"

JARVIS will give a short summary if a Wikipedia page is available.

##Contacts

JARVIS can store alternative names for contacts.

#For example:

"Hey Jarvis, add contact Rahul as Bhai"

You can also use a person's WhatsApp number.

If JARVIS asks for information that you would rather type, say "written" and enter it through the keyboard.

##Troubleshooting

JARVIS doesn't hear me: Check your microphone, Windows microphone permissions, and make sure you're saying the wake word clearly.

An application doesn't open: Check its path in apps.json.

WhatsApp features don't work: Make sure WhatsApp Desktop is installed and check the relevant coordinates in coords.json.

The mouse clicks the wrong place: Run coord_test.py and reconfigure the coordinates.

##Privacy

JARVIS may use files such as clients.json, contacts.json, and notes.json to store information.

Do not upload real client information, personal contact information, passwords, API keys, or other private data to a public GitHub repository.

If you're publishing JARVIS, use empty/example JSON files instead.

Enjoy!

JARVIS v0.1 — Built in Python.
