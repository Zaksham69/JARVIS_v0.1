JARVIS v0.1

JARVIS v0.1 is a simple, non-AI, voice-controlled PC assistant built in Python.

How to Use
1. Install the required modules

Make sure all Python modules used by JARVIS are installed before running the program.

The required modules include:

pyttsx3
SpeechRecognition
PyAutoGUI
Wikipedia
PyAudio

JARVIS also requires a working microphone.

Note: Speech recognition and Wikipedia require an internet connection.

2. Configure apps.json

Open apps.json.

For each application, enter the application's .exe location or its Windows Target alongside the app's name. The app names must be written in ALL CAPS.

To find an application's Target:

Right-click the application's shortcut.
Select Properties.
Select the Target field, if it is selectable.
Copy the Target and paste it into apps.json.

If the Target field cannot be selected, take a screenshot of the Properties window and use an image-to-text tool to extract the Target text. You can use ImageToText.info for this if needed: ImageToText.info

After entering the path, replace every \ with \\ in the JSON file.

For example, C:\Program Files\App\App.exe becomes C:\\Program Files\\App\\App.exe.

Important: If an application is moved or reinstalled, its path may change. Update apps.json if this happens.

3. Configure coords.json

Open coords.json.

For each required section, enter the X and Y mouse coordinates.

After entering the coordinates, run coord_test.py to check whether they are correct.

Important: Mouse coordinates depend on your screen resolution, display scaling, and the position of elements on your screen. Coordinates that work on one computer may not work correctly on another.

If you don't have Minecraft installed, you can ignore the Minecraft coordinates.

4. Configure WhatsApp

Make sure the WhatsApp Desktop application is installed on your PC.

JARVIS uses the desktop version for features such as calling and messaging.

Using JARVIS

JARVIS requires a wake word before commands.

Say "Hey Jarvis" or simply "Jarvis" before every command. If you do not say the wake word, JARVIS will ignore the command.

Wikipedia

You can ask JARVIS to search Wikipedia.

Example: "Hey Jarvis, Wikipedia Albert Einstein"

JARVIS will return a short, approximately two-line summary of the Wikipedia page, if one exists.

Contacts

JARVIS can store alternative names for contacts.

For example, if someone is saved as Rahul but you normally call them Bhai, you can say:

"Hey Jarvis, add contact Rahul as Bhai"

You can also use the person's WhatsApp number instead of their saved name.

If you want to type the information instead of speaking it, say "written" when JARVIS asks for it.

Important Tips
Always say "Jarvis" or "Hey Jarvis" before your command.
Make sure your microphone is working.
Make sure WhatsApp Desktop is installed.
Make sure the paths in apps.json are correct.
Test your coordinates using coord_test.py before using mouse-controlled features.
Keep the required JSON files in the correct location alongside JARVIS.
Make sure your screen resolution and display scaling have not changed after configuring your coordinates.
If you move or reinstall an application, check and update its path in the appropriate JSON file.
JARVIS requires an internet connection for speech recognition and Wikipedia features.
Privacy and Security

JARVIS may store information in JSON files such as clients.json, contacts.json, and notes.json. These files may contain personal or sensitive information.

Do not upload real client information, personal contact information, passwords, API keys, or other private data to a public GitHub repository.

If you are publishing JARVIS on GitHub, use empty or example JSON files instead. You can also add private files to .gitignore so Git does not upload them.

Troubleshooting

JARVIS does not hear me: Check that your microphone is connected, Windows has microphone permission enabled, the correct microphone is selected, and that you are speaking the wake word clearly.

JARVIS does not open an application: Check the application's entry in apps.json and make sure the path is correct.

WhatsApp features do not work correctly: Make sure WhatsApp Desktop is installed, check the coordinates in coords.json, run coord_test.py, and make sure the WhatsApp window layout matches the layout used when the coordinates were configured.

Mouse-controlled features click the wrong place: Run coord_test.py and reconfigure the coordinates in coords.json.

Enjoy!

Your JARVIS v0.1 setup is complete.

Have fun using it, experimenting with it, and adding your own features!

JARVIS v0.1 — Built in Python.
