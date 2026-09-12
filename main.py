import os
import sys
import json
import hashlib
import subprocess
import webbrowser
import datetime
import time as _Time
from pathlib import Path

import pyautogui
import wikipedia

# =========================================================
# PROJECT PATHS
# =========================================================
SCRIPT_DIR = Path(__file__).resolve().parent

CONFIG_DIR = SCRIPT_DIR / "Configurates"
IMAGES_DIR = SCRIPT_DIR / "images"
TEXT_FILES_DIR = SCRIPT_DIR / "textFiles"

APPS_FILE = CONFIG_DIR / "apps.json"
CLIENTS_FILE = CONFIG_DIR / "clients.json"
CONTACTS_FILE = CONFIG_DIR / "contacts.json"
COORDS_FILE = CONFIG_DIR / "coords.json"

PASSWORD_FILE = TEXT_FILES_DIR / "password.txt"
NOTES_FILE = CONFIG_DIR / "notes.json"

# Make relative paths inside functions.py resolve from the project root.
os.chdir(SCRIPT_DIR)
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import functions as fn


# =========================================================
# SYNC PATHS WITH functions.py
# =========================================================
# This lets main.py work with the folder layout in the screenshot
# even if functions.py still uses these variable names.
for _name, _value in {
    "SCRIPT_DIR": SCRIPT_DIR,
    "APPS_FILE": APPS_FILE,
    "CLIENTS_FILE": CLIENTS_FILE,
    "CONTACTS_FILE": CONTACTS_FILE,
    "COORDS_FILE": COORDS_FILE,
    "NOTES_FILE": NOTES_FILE,
    "CONFIG_DIR": CONFIG_DIR,
    "IMAGES_DIR": IMAGES_DIR,
    "TEXT_FILES_DIR": TEXT_FILES_DIR,
}.items():
    if hasattr(fn, _name):
        setattr(fn, _name, _value)


# =========================================================
# HELPERS
# =========================================================
def load_json_file(path, default=None):
    if default is None:
        default = {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json_file(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Load the files from Configurates explicitly.
APPS = load_json_file(APPS_FILE, {})
CONTACTS = load_json_file(CONTACTS_FILE, {})
COORDS = load_json_file(COORDS_FILE, {})

# Keep functions.py's globals in sync when they exist.
for _name, _value in {
    "APPS": APPS,
    "CONTACTS": CONTACTS,
    "COORDS": COORDS,
}.items():
    if hasattr(fn, _name):
        setattr(fn, _name, _value)

# Import the functions used by main.py without importing every name
# into the global namespace.
home_screen = fn.home_screen
listen = fn.listen
ask_field = fn.ask_field
sayywrite = fn.sayywrite
say = fn.say
call = fn.call
locate = fn.locate
locate_all = fn.locate_all
print_noteFamily = fn.print_noteFamily
return_noteFamily = fn.return_noteFamily
WAKE_WORDS = getattr(fn, "WAKE_WORDS", ("jarvis", "jervis"))


# =========================================================
# PASSWORD / FIRST-RUN SETUP
# =========================================================
def read_security_file():
    """
    password.txt format:
        launch_count, sha256_hash, theme

    The theme part is optional so old password.txt files still work.
    """
    if not PASSWORD_FILE.exists():
        return 0, "", None

    try:
        content = PASSWORD_FILE.read_text(encoding="utf-8").strip()
        parts = [part.strip() for part in content.split(",", 2)]

        if len(parts) < 2:
            return 0, "", None

        try:
            launch_count = int(parts[0])
        except ValueError:
            launch_count = 0

        password_hash = parts[1]
        theme = parts[2].lower() if len(parts) >= 3 else None

        if theme not in ("dark", "light"):
            theme = None

        return launch_count, password_hash, theme

    except OSError:
        return 0, "", None


def write_security_file(launch_count, password_hash, theme):
    PASSWORD_FILE.write_text(
        f"{launch_count}, {password_hash}, {theme}\n",
        encoding="utf-8",
    )


times_open, stored_password_hash, theme = read_security_file()

home_screen()

# First run, or an old password file without a saved theme.
if times_open == 0 or not stored_password_hash:
    while True:
        password = ask_field(
            "Enter your PC password for confirmations like shutdown"
        )

        if password is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        password = password.strip()

        if not password:
            sayywrite("Password cannot be empty.")
            continue

        stored_password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        break

if theme is None:
    while True:
        theme_answer = ask_field(
            "Are you using Dark theme or light theme on your PC?"
        )

        if theme_answer is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        theme_answer = theme_answer.lower()

        if "dark" in theme_answer:
            theme = "dark"
            break

        if "light" in theme_answer:
            theme = "light"
            break

        sayywrite(
            "Please answer 'dark theme' or 'light theme' as per your PC settings."
        )

    sayywrite(
        "Kindly remove your hands from your keyboard or mouse. "
        "Configuring coordinates."
    )
    _Time.sleep(5)
    locate_all(theme)

# Count this launch only after the setup information is valid.
times_open += 1
write_security_file(times_open, stored_password_hash, theme)


# =========================================================
# MAIN LOOP
# =========================================================
while True:
    cmd = listen()

    if not cmd:
        continue

    cmd = cmd.strip().lower()

    # -----------------------------------------------------
    # WAKE WORD
    # -----------------------------------------------------
    if not any(word in cmd for word in ("jarvis", "jervis")):
        continue

    for wake in WAKE_WORDS:
        wake = wake.lower()
        if cmd.startswith(wake):
            cmd = cmd[len(wake):].strip()
            break

    if not cmd:
        sayywrite("How can I help you?")
        continue

    print("Command:", cmd)

    # =====================================================
    # MINECRAFT
    # =====================================================
    if "minecraft" in cmd:
        delay = False

        while True:
            locateMC = locate(theme, "image4.png", "MINECRAFT")
            locateUpY = locate(
                theme, "image5.png", "MINECRAFT_UPTADE_BUTTON_YES"
            )
            locateUpN = locate(
                theme, "image6.png", "MINECRAFT_UPTADE_BUTTON_NO"
            )

            if locateMC is None:
                if locateUpY == "Done":
                    sayywrite("A Tlauncher update is available.")

                    while True:
                        updateYN = ask_field("Would you like me to update it?")

                        if updateYN is None:
                            sayywrite("Sorry, I didn't catch that.")
                            continue

                        updateYN = updateYN.lower()

                        if "yes" in updateYN:
                            sayywrite("Updating Tlauncher.")
                            delay = True
                            pyautogui.moveTo(
                                *COORDS["MINECRAFT_UPTADE_BUTTON_YES"]
                            )
                            pyautogui.click()
                            break

                        sayywrite("That would be counted as a no.")
                        pyautogui.moveTo(
                            *COORDS["MINECRAFT_UPTADE_BUTTON_NO"]
                        )
                        pyautogui.click()
                        break

                if delay:
                    _Time.sleep(150)
                    continue

                _Time.sleep(0.2)
                continue

            if locateMC == "Done":
                pyautogui.moveTo(*COORDS["MINECRAFT"])
                pyautogui.click()
                break

            _Time.sleep(0.2)

    # =====================================================
    # OPEN
    # =====================================================
    elif cmd.startswith("open "):
        app = cmd[5:].strip().upper()

        if app == "GOOGLE":
            app = "CHROME"

        if app in APPS:
            value = APPS[app]

            if isinstance(value, list):
                subprocess.Popen(value)

            elif isinstance(value, str) and value.endswith("!App"):
                subprocess.Popen(
                    ["explorer.exe", f"shell:AppsFolder\\{value}"]
                )

            elif isinstance(value, str):
                try:
                    os.startfile(value)
                except OSError as e:
                    print(e)
                    sayywrite(f"I couldn't open {app}.")
        else:
            # Unknown names are treated as websites.
            website = app.lower().strip()

            if "." in website:
                if website.startswith(("www.", "web.")):
                    url = f"https://{website}"
                else:
                    url = f"https://{website}"
            else:
                url = f"https://www.{website}.com"

            webbrowser.open(url)

    # =====================================================
    # CALL
    # =====================================================
    elif cmd.startswith("call "):
        name = cmd[5:].strip()
        contact = CONTACTS.get(name, name)
        call(contact)

    # =====================================================
    # TIME
    # =====================================================
    elif cmd == "time" or "what time" in cmd:
        now = datetime.datetime.now()
        sayywrite(f"The time is {now.strftime('%I:%M %p')}")

    # =====================================================
    # DATE
    # =====================================================
    elif cmd == "date" or "what date" in cmd or "today's date" in cmd:
        now = datetime.datetime.now()
        sayywrite(f"The date is {now.strftime('%A %d %B %Y')}")

    # =====================================================
    # WIKIPEDIA
    # =====================================================
    elif "wikipedia" in cmd:
        query = cmd.replace("wikipedia", "", 1).strip()

        if not query:
            sayywrite("What should I search on Wikipedia?")
            continue

        try:
            result = wikipedia.summary(query, sentences=2)
            sayywrite(result)
        except Exception as e:
            print(e)
            sayywrite("Sorry, I couldn't find information.")

    # =====================================================
    # GOOGLE SEARCH
    # =====================================================
    elif "search google" in cmd:
        query = cmd.replace("search google", "", 1).strip()

        if not query:
            sayywrite("What should I search for?")
            continue

        try:
            chrome = APPS["CHROME"]

            if isinstance(chrome, list):
                subprocess.Popen(chrome)
            elif isinstance(chrome, str):
                os.startfile(chrome)
            else:
                raise ValueError("Invalid CHROME configuration.")

        except (KeyError, OSError, ValueError) as e:
            print(e)
            sayywrite("Chrome is not configured correctly in Configurates/apps.json.")
            continue

        _Time.sleep(2)

        if "CHROME_SEARCH_BOX" not in COORDS:
            sayywrite("Chrome search-box coordinates are not configured.")
            continue

        pyautogui.moveTo(*COORDS["CHROME_SEARCH_BOX"])
        pyautogui.click()
        pyautogui.write(query, interval=0.01)
        pyautogui.press("enter")

    # =====================================================
    # SHUTDOWN
    # =====================================================
    elif "shutdown" in cmd:
        confirm = ask_field("Password")

        if confirm:
            confirm_hash = hashlib.sha256(
                confirm.strip().encode("utf-8")
            ).hexdigest()

            if confirm_hash == stored_password_hash:
                pyautogui.hotkey("win", "x")
                pyautogui.press("u")
                pyautogui.press("u")
            else:
                sayywrite("Incorrect password. Cancelled.")
        else:
            sayywrite("Cancelled.")

    # =====================================================
    # ADD CONTACT
    # =====================================================
    elif "add contact" in cmd:
        try:
            parts = (
                cmd.replace("add contact", "", 1)
                .strip()
                .split(" as ", 1)
            )

            if len(parts) != 2:
                raise ValueError("Invalid contact format.")

            nickname = parts[0].strip()
            name = parts[1].strip()

            if nickname == "written":
                nickname = input("Contact: ").strip()

            if not name or not nickname:
                raise ValueError("Name or nickname is empty.")

            CONTACTS[name] = nickname
            save_json_file(CONTACTS_FILE, CONTACTS)

            if hasattr(fn, "CONTACTS"):
                fn.CONTACTS = CONTACTS

            sayywrite("Contact added.")

        except Exception as e:
            print(e)
            sayywrite("Say: add contact [number] as [nickname]")

    # =====================================================
    # ADD CLIENT
    # =====================================================
    elif "add client" in cmd:
        clients = fn.load_clients()
        client = cmd.replace("add client", "", 1).strip()

        if not client:
            sayywrite("Please provide the client name.")
            continue

        email = ask_field("Email")
        if email is None:
            sayywrite("Client was not added.")
            continue

        number = ask_field("Phone number/Whatsapp number (if any)")

        phone = ""
        whatsapp = ""

        if number:
            number = number.strip()

            if "/" in number:
                phone, whatsapp = [part.strip() for part in number.split("/", 1)]
            else:
                phone = number

        passport = ask_field("Passport") or ""
        visa = ask_field("Visa") or ""
        destination = ask_field("Destination") or ""

        notes = []

        sayywrite("Are there any extra or personal notes on this client?")
        notes_cfrm = listen()

        if notes_cfrm and "yes" in notes_cfrm.lower():
            note = ask_field("Your Note")

            while note:
                if note.lower() == "no":
                    break

                notes.append(note)
                note = ask_field("Any other note")

        clients[client] = {
            "Email": email,
            "Phone": phone,
            "Whatsapp": whatsapp,
            "Passport": passport,
            "Visa": visa,
            "Destination": destination,
            "Notes": notes,
        }

        fn.save_clients(clients)
        sayywrite(f"{client} has been added and updated.")

    # =====================================================
    # EDIT CLIENT
    # =====================================================
    elif "edit client" in cmd:
        clients = fn.load_clients()
        client = cmd.replace("edit client", "", 1).strip()

        if client not in clients:
            sayywrite("Client not found.")
            continue

        sayywrite("Which field?")
        field = listen()

        if field is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        field_map = {
            "email": "Email",
            "phone": "Phone",
            "whatsapp": "Whatsapp",
            "passport": "Passport",
            "visa": "Visa",
            "destination": "Destination",
            "notes": "Notes",
        }

        field_key = field_map.get(field.lower().strip())

        if field_key is None:
            sayywrite("That field doesn't exist.")
            continue

        value = ask_field("Value?")

        if value is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        if field_key == "Notes":
            clients[client][field_key] = [value]
        else:
            clients[client][field_key] = value

        fn.save_clients(clients)
        sayywrite("Client edited.")

    # =====================================================
    # SHOW CLIENT
    # =====================================================
    elif "show client" in cmd:
        clients = fn.load_clients()
        client = cmd.replace("show client", "", 1).strip()

        if client not in clients:
            sayywrite("Client not found.")
            continue

        sayywrite("Which field?")
        field = listen()

        if field is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        field = field.lower().strip()

        if field in ("all", "all fields"):
            print(clients[client])

            sayywrite(
                "Would you like me to recite it for you? "
                "Or show it in a file?"
            )

            confirm = listen()

            if confirm is None:
                sayywrite("Sorry, I didn't catch that.")
                continue

            confirm = confirm.lower()

            if "recite" in confirm or confirm == "yes":
                for key, value in clients[client].items():
                    sayywrite(f"{key}: {value}")

            elif "file" in confirm:
                TEXT_FILES_DIR.mkdir(parents=True, exist_ok=True)
                client_file = TEXT_FILES_DIR / "client.txt"

                with open(client_file, "w", encoding="utf-8") as file:
                    file.write(f"Client: {client}\n\n")
                    for key, value in clients[client].items():
                        file.write(f"{key}: {value}\n")

                os.startfile(client_file)

        else:
            field_map = {
                "email": "Email",
                "phone": "Phone",
                "whatsapp": "Whatsapp",
                "passport": "Passport",
                "visa": "Visa",
                "destination": "Destination",
                "notes": "Notes",
            }

            field_key = field_map.get(field)

            if field_key is None:
                sayywrite("The field doesn't exist.")
            else:
                sayywrite(str(clients[client].get(field_key, "")))

    # =====================================================
    # SEARCH FIELD
    # =====================================================
    elif "search field" in cmd:
        clients = fn.load_clients()

        query = cmd.replace("search field", "", 1).strip()
        field = query

        value = ask_field("Value?")

        if value is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        field_map = {
            "email": "Email",
            "phone": "Phone",
            "whatsapp": "Whatsapp",
            "passport": "Passport",
            "visa": "Visa",
            "destination": "Destination",
        }

        field = field_map.get(field.lower(), field)

        matches = []

        for client_name, client_data in clients.items():
            if str(client_data.get(field, "")).lower() == str(value).lower():
                matches.append(client_name)

        if matches:
            sayywrite("Matching clients: " + ", ".join(matches))
        else:
            sayywrite("Client not detected.")

    # =====================================================
    # ADD NOTE FAMILY
    # =====================================================
    elif "add note family" in cmd:
        note_family = cmd.replace("add note family", "", 1).strip()

        if not note_family:
            sayywrite("Please provide the note family name.")
            continue

        notes = fn.load_notes()

        if note_family in notes:
            sayywrite(
                "Note family already exists. Would you like me to replace it?"
            )
            replace_yn = listen()

            if replace_yn is None:
                sayywrite("Sorry, I didn't catch that.")
                continue

            if "yes" not in replace_yn.lower():
                sayywrite("Keeping the existing note family.")
                continue

        notes[note_family] = []

        sayywrite(
            "Note family added. Would you like to enter your first note in it?"
        )
        confirm_note = listen()

        if confirm_note is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        if "yes" in confirm_note.lower():
            sayywrite(f"What is your first note in {note_family}?")
            note = listen()

            if note:
                notes[note_family].append(note)

        fn.save_notes(notes)

    # =====================================================
    # ADD NOTE
    # =====================================================
    elif "add note" in cmd:
        notes = fn.load_notes()
        query = cmd.replace("add note", "", 1).strip()

        marker = " in note family "

        if marker in query:
            note, note_family = query.split(marker, 1)
            note = note.strip()
            note_family = note_family.strip()
        else:
            note = query
            note_family = ask_field("Note family?")

        if not note or not note_family:
            sayywrite("Note or note family is missing.")
            continue

        if note_family not in notes:
            sayywrite("Note family does not exist.")
            continue

        if note in notes[note_family]:
            sayywrite("Note already exists. Do you want to replace it?")
            confirm = listen()

            if confirm is None:
                sayywrite("Sorry, I didn't catch that.")
                continue

            if "yes" not in confirm.lower():
                sayywrite("That would be taken as a no.")
                continue

            # It is already present, so there is nothing useful to append.
            sayywrite("The note is already saved.")

        else:
            notes[note_family].append(note)
            fn.save_notes(notes)
            sayywrite("Note added.")

    # =====================================================
    # SHOW NOTE FAMILY
    # =====================================================
    elif "show note family" in cmd:
        notes = fn.load_notes()
        note_family = cmd.replace("show note family", "", 1).strip()

        if note_family not in notes:
            sayywrite("Note family does not exist.")
            continue

        print_noteFamily(note_family)

        sayywrite(
            "Note family printed. Would you like me to recite it "
            "or show it in a file?"
        )

        show = listen()

        if show is None:
            sayywrite("Sorry, I didn't catch that.")
            continue

        show = show.lower()

        if "recite" in show or show == "yes":
            for note in notes[note_family]:
                sayywrite(str(note))

        elif "file" in show:
            TEXT_FILES_DIR.mkdir(parents=True, exist_ok=True)
            note_file = TEXT_FILES_DIR / "noteFamily.txt"

            with open(note_file, "w", encoding="utf-8") as file:
                file.write(f"{note_family}->\n")
                file.write(return_noteFamily(note_family))

            os.startfile(note_file)

    # =====================================================
    # EXIT
    # =====================================================
    elif cmd == "exit" or "exit" in cmd:
        sayywrite("Goodbye!")
        break
