JARVIS v0.1

JARVIS v0.1 is a simple, non-AI, voice-controlled PC assistant built in Python.

How to Use
1. Install the required modules

Make sure all Python modules used by JARVIS are installed before running the program.

2. Configure apps.json

Open apps.json.

For each app, enter the application's .exe location or its Windows Target alongside the app's name.

The app names must be written in ALL CAPS.

Example:

{
    "VSCODE": "C:\\Path\\To\\Code.exe",
    "CHROME": "C:\\Path\\To\\Chrome.exe"
}
How to find an application's Target
Right-click the app's shortcut.
Select Properties.
Select the Target field, if it is selectable.
Copy the Target and paste it into apps.json.

If the Target field cannot be selected:

Take a screenshot of the Properties window.
Use an image-to-text tool to extract the Target text.
Copy the extracted text into apps.json.

After entering the path, replace Windows backslashes with double backslashes for JSON.

For example:

C:\Program Files\App\App.exe

becomes:

C:\\Program Files\\App\\App.exe
3. Configure coords.json

Open coords.json.

For each required section, enter the X and Y mouse coordinates.

For example:

{
    "WHATSAPP_SEARCH_BOX": [150, 120],
    "WHATSAPP_FIRST_RESULT": [150, 270],
    "WHATSAPP_CALL_BUTTON": [1775, 70]
}

After entering the coordinates, run:

coord_test.py

Use the coordinate tester to check whether your coordinates are correct.

If you don't have Minecraft installed, you can ignore the Minecraft coordinates.

4. Configure WhatsApp

Make sure the WhatsApp Desktop application is installed on your PC.

JARVIS uses the desktop version for features such as calling and messaging.

Using JARVIS

JARVIS requires a wake word before commands.

Wake Word

Say:

"Hey Jarvis"

or simply:

"Jarvis"

before every command.

Wikipedia

You can ask JARVIS to search Wikipedia.

Example:

"Hey Jarvis, Wikipedia Albert Einstein"

JARVIS will return a short, approximately two-line summary of the Wikipedia page, if one exists.

Contacts

JARVIS can store alternative names for contacts.

For example, if someone is saved as:

Rahul

but you normally call them:

Bhai

you can say:

"Hey Jarvis, add contact Rahul as Bhai"

You can also use the person's WhatsApp number instead of their saved name.

If you want to type the information instead of speaking it, say:

"written"

when JARVIS asks for it.

Important Tips
Always say "Jarvis" or "Hey Jarvis" before your command.
Make sure your microphone is working.
Make sure WhatsApp Desktop is installed.
Make sure the paths in apps.json are correct.
Test your coordinates using coord_test.py before using mouse-controlled features.
Keep the required JSON files in the correct location alongside JARVIS.

Enjoy!

Your JARVIS v0.1 setup is complete.

Have fun using it and adding your own features!
