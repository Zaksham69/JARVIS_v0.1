import datetime
import hashlib
import os
import subprocess
import time as _Time
import webbrowser
import pyautogui
import wikipedia
from functions import *

# =========================================================
# PASSWORD / OPEN COUNT
# =========================================================

PASSWORD_FILE = SCRIPT_DIR / "password.txt"

times_open = 0
hashed_password = None

if PASSWORD_FILE.exists():
    with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()

    if ", " in content:
        i = content.find(", ")
        try:
            times_open = int(content[:i])
            hashed_password = content[i + 2:].strip()
        except ValueError:
            times_open = 0
            hashed_password = None
    else:
        times_open = 0
        hashed_password = None

# =========================================================
# STARTUP
# =========================================================

home_screen()

if times_open == 0 or not hashed_password:
    password = ask_field("Enter your PC password for confirmations like shutdown")

    if password is None:
        sayywrite("Sorry, I didn't catch that.")
        raise SystemExit

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    times_open = 1
else:
    times_open += 1

# Save updated opening count and password hash
with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
    file.write(f"{times_open}, {hashed_password}")

# =========================================================
# MAIN LOOP
# =========================================================

while True:
    cmd = listen()

    if not cmd:
        continue

    # -----------------------------------------------------
    # WAKE WORD
    # -----------------------------------------------------

    if not any(word in cmd for word in ("jarvis", "jervis")):
        continue

    for wake in WAKE_WORDS:
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
        sayywrite("Opening Minecraft")

        try:
            os.startfile(APPS["TLAUNCHER"])
        except KeyError:
            sayywrite("TLauncher is not configured in apps.json.")
            continue

        _Time.sleep(45)

        try:
            move(*COORDS["MINECRAFT"])
            pyautogui.click()
        except KeyError:
            sayywrite("Minecraft coordinates are not configured.")
            continue

    # =====================================================
    # OPEN
    # =====================================================

    elif cmd.startswith("open"):
        app = cmd.replace("open", "", 1).strip().upper()

        if app == "GOOGLE":
            app = "CHROME"

        if app in APPS:
            value = APPS[app]

            # Chrome profile / command list
            if isinstance(value, list):
                subprocess.Popen(value)

            # Microsoft Store app
            elif isinstance(value, str) and value.endswith("!App"):
                subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{value}"])

            # Normal executable
            elif isinstance(value, str):
                os.startfile(value)

        else:
            dot_index = -1

            for i in range(len(app)):
                if app[i] == ".":
                    dot_index = i
                    break

            # A dot exists
            if dot_index != -1:
                # Possible pre-domain such as www., web., etc.
                if dot_index <= 3:
                    # Another dot exists after the first one
                    if "." in app[dot_index + 1:]:
                        webbrowser.open(f"https://{app.lower()}")
                    else:
                        webbrowser.open(f"https://{app.lower()}.com")
                else:
                    webbrowser.open(f"https://www.{app.lower()}")
            # No dot
            else:
                webbrowser.open(f"https://www.{app.lower()}.com")

    # =====================================================
    # CALL
    # =====================================================

    elif "call" in cmd:
        name = cmd.replace("call", "", 1).strip()
        contact = CONTACTS.get(name, name)
        call(contact)

    # =====================================================
    # TIME
    # =====================================================

    elif "time" in cmd:
        now = datetime.datetime.now()
        sayywrite(f"The time is {now.strftime('%I:%M %p')}")

    # =====================================================
    # DATE
    # =====================================================

    elif "date" in cmd:
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
            value = APPS["CHROME"]
            if isinstance(value, list):
                subprocess.Popen(value)
            else:
                subprocess.Popen(value)
        except KeyError:
            sayywrite("Chrome is not configured in apps.json.")
            continue

        _Time.sleep(2)

        try:
            move(*COORDS["CHROME_SEARCH_BOX"])
            pyautogui.click()
            write(query)
            pyautogui.press("enter")
        except KeyError:
            sayywrite("Chrome search coordinates are not configured.")

    # =====================================================
    # SHUTDOWN
    # =====================================================

    elif "shutdown" in cmd:
        confirm = ask_field("Password")

        if confirm is None:
            sayywrite("Cancelled")
            continue

        entered_hash = hashlib.sha256(confirm.encode()).hexdigest()

        if entered_hash == hashed_password:
            sayywrite("Password accepted.")
            pyautogui.hotkey("win", "x")
            pyautogui.press("u")
            pyautogui.press("u")
        else:
            sayywrite("Incorrect password. Cancelled.")

    # =====================================================
    # ADD CONTACT
    # =====================================================

    elif "add contact" in cmd:
        try:
            parts = cmd.replace("add contact", "", 1).strip().split(" as ")
            nickname = parts[0].strip()
            name = parts[1].strip()

            if nickname == "written":
                nickname = input("Contact: ").strip()

            CONTACTS[name] = nickname
            save_json(CONTACTS_FILE, CONTACTS)
            sayywrite("Contact added.")
        except Exception as e:
            print(e)
            sayywrite("Say: add contact [number] as [nickname]")

    # =====================================================
    # ADD CLIENT
    # =====================================================

    elif "add client" in cmd:
        clients = load_clients()
        client = cmd.replace("add client", "", 1).strip()

        if not client:
            sayywrite("Please provide the client name.")
            continue

        # Email
        email = ask_field("Email")
        if email is None:
            sayywrite("Client was not added.")
            continue

        # Phone / WhatsApp
        number = ask_field("Phone number/Whatsapp number (if any)")
        phone = ""
        whatsapp = ""

        if number:
            number = number.strip()
            if "/" in number:
                i = number.find("/")
                phone = number[:i].strip()
                whatsapp = number[i + 1:].strip()
            else:
                phone = number

        # Notes
        notes = []
        sayywrite("Are there any extra or personal notes on this client?")
        notes_cfrm = listen()

        if notes_cfrm and "yes" in notes_cfrm.lower():
            note = ask_field("Your Note")
            if note:
                while note.lower() != "no":
                    notes.append(note)
                    note = ask_field("Any other note")
                    if note is None:
                        break

        # Save Client
        clients[client] = {
            "Email": email,
            "Phone": phone,
            "Whatsapp": whatsapp,
            "Passport": "",
            "Destination": "",
            "Visa": "",
            "Notes": notes
        }

        save_clients(clients)
        sayywrite(f"{client} has been added and updated.")

    # =====================================================
    # EDIT CLIENT
    # =====================================================

    elif "edit client" in cmd:
        clients = load_clients()
        client = cmd.replace("edit client", "", 1).strip()

        if client not in clients:
            sayywrite("Client not found.")
            continue

        sayywrite("Which field?")
        field = listen()

        if field is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        field = field.strip()
        field_map = {
            "email": "Email",
            "phone": "Phone",
            "whatsapp": "Whatsapp",
            "passport": "Passport",
            "destination": "Destination",
            "visa": "Visa",
            "notes": "Notes"
        }

        field_key = field_map.get(field.lower())

        if field_key is None:
            sayywrite("That field doesn't exist.")
            continue

        sayywrite("Value?")
        value = listen()

        if value is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        if field_key == "Notes":
            clients[client][field_key] = [value]
        else:
            clients[client][field_key] = value

        save_clients(clients)
        sayywrite("Client edited.")

    # =====================================================
    # SHOW CLIENT - ALL FIELDS
    # =====================================================

    elif "show client all fields" in cmd:
        clients = load_clients()
        client = cmd.replace("show client all fields", "", 1).strip()

        if client not in clients:
            sayywrite("Client not found.")
            continue

        print(clients[client])
        sayywrite("Would you like me to recite it for you? Or show it in a file?")

        confirm = listen()
        if confirm is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        confirm = confirm.lower()

        if "yes" in confirm:
            for key, value in clients[client].items():
                sayywrite(f"{key}: {value}")

        elif "show it in a file" in confirm:
            sayywrite("Opening client.txt")
            client_file = SCRIPT_DIR / "client.txt"

            with open(client_file, "w", encoding="utf-8") as file:
                file.write(f"Client: {client}\n\n")
                for key, value in clients[client].items():
                    file.write(f"{key}: {value}\n")

            os.startfile(client_file)

    # =====================================================
    # SHOW CLIENT - SINGLE FIELD
    # =====================================================

    elif "show client" in cmd:
        clients = load_clients()
        client = cmd.replace("show client", "", 1).strip()

        if client not in clients:
            sayywrite("Client not found.")
            continue

        sayywrite("Which field?")
        field = listen()

        if field is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        field = field.lower().strip()

        if field in ("all", "all fields"):
            print(clients[client])
            sayywrite("Would you like me to recite it for you? Or show it in a file?")

            confirm = listen()
            if confirm is None:
                sayywrite("Sorry I didn't catch that.")
                continue

            confirm = confirm.lower()

            if "yes" in confirm:
                for key, value in clients[client].items():
                    sayywrite(f"{key}: {value}")

            elif "show it in a file" in confirm:
                sayywrite("Opening client.txt")
                client_file = SCRIPT_DIR / "client.txt"

                with open(client_file, "w", encoding="utf-8") as file:
                    file.write(f"Client: {client}\n\n")
                    for key, value in clients[client].items():
                        file.write(f"{key}: {value}\n")

                os.startfile(client_file)

        elif field == "email":
            sayywrite(clients[client].get("Email", ""))

        elif field == "phone" or "phone" in field:
            sayywrite(clients[client].get("Phone", ""))

        elif field == "whatsapp" or "whatsapp" in field:
            sayywrite(clients[client].get("Whatsapp", ""))

        elif field == "passport":
            sayywrite(clients[client].get("Passport", ""))

        elif field == "destination":
            sayywrite(clients[client].get("Destination", ""))

        elif field == "visa":
            sayywrite(clients[client].get("Visa", ""))

        elif field == "notes":
            sayywrite(str(clients[client].get("Notes", [])))

        else:
            sayywrite("The field doesn't exist.")

    # =====================================================
    # SEARCH FIELD
    # =====================================================

    elif "search field" in cmd:
        clients = load_clients()
        field = cmd.replace("search field", "", 1).strip()

        value = ask_field("Value?")

        if value is None:
            sayywrite("Sorry, I didn't catch the value.")
            continue

        field_map = {
            "email": "Email",
            "phone": "Phone",
            "whatsapp": "Whatsapp",
            "passport": "Passport",
            "destination": "Destination",
            "visa": "Visa"
        }

        field_key = field_map.get(field.lower())

        if field_key is None:
            sayywrite("That field doesn't exist.")
            continue

        found_client = None

        for client_name, client_data in clients.items():
            if str(client_data.get(field_key, "")).lower() == value.lower():
                found_client = client_name
                break

        if found_client is None:
            sayywrite("Client not detected.")
        else:
            sayywrite(f"Client found: {found_client}")

    # =====================================================
    # ADD NOTE FAMILY
    # =====================================================

    elif "add note family" in cmd:
        noteFamily = cmd.replace("add note family", "", 1).strip()

        if not noteFamily:
            sayywrite("Please provide a note family name.")
            continue

        notes = load_notes()

        if noteFamily in notes:
            sayywrite("Note family already exists. Would you like me to replace it?")
            replaceYN = listen()

            if replaceYN is None:
                sayywrite("Sorry I didn't catch that.")
                continue

            if "yes" in replaceYN.lower():
                notes[noteFamily] = []
            else:
                continue
        else:
            notes[noteFamily] = []

        sayywrite("Note family added. Would you like to enter your first note in it?")
        confirm_note = listen()

        if confirm_note is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        if "yes" in confirm_note.lower():
            sayywrite(f"What is your first note in {noteFamily}?")
            note = listen()

            if note is None:
                sayywrite("Sorry I didn't catch that.")
                continue

            notes[noteFamily].append(note)

        save_notes(notes)

    # =====================================================
    # ADD NOTE
    # =====================================================

    elif "add note" in cmd:
        notes = load_notes()
        query = cmd.replace("add note", "", 1).strip()

        if " in note family " in query:
            i = query.find(" in note family ")
            note = query[:i].strip()
            noteFamily = query[i + len(" in note family "):].strip()
        else:
            note = query
            noteFamily = ask_field("Note family?")

            if noteFamily is None:
                sayywrite("Sorry, I didn't catch that.")
                continue

        if noteFamily not in notes:
            sayywrite("Note family does not exist.")
            continue

        if note in notes[noteFamily]:
            sayywrite("Note already exists. Do you want me to replace it?")
            confirm = listen()

            if confirm is None:
                sayywrite("Sorry, I didn't catch that.")
                continue

            if "yes" in confirm.lower():
                notes[noteFamily].remove(note)
            else:
                sayywrite("That would be taken as a no.")
                continue

        notes[noteFamily].append(note)
        save_notes(notes)
        sayywrite("Note added.")

    # =====================================================
    # SHOW NOTE FAMILY
    # =====================================================

    elif "show note family" in cmd:
        notes = load_notes()
        noteFamily = cmd.replace("show note family", "", 1).strip()

        if noteFamily not in notes:
            sayywrite("Note family does not exist.")
            continue

        print_noteFamily(noteFamily)
        sayywrite("Note Family printed. Would you like me to recite it for you, or show it in a file?")

        show = listen()

        if show is None:
            sayywrite("Sorry I didn't catch that.")
            continue

        show = show.lower()

        if "recite" in show or "yes" in show:
            for note in notes[noteFamily]:
                sayywrite(note)

        elif "file" in show:
            sayywrite("Opening noteFamily.txt")
            note_file = SCRIPT_DIR / "noteFamily.txt"

            with open(note_file, "w", encoding="utf-8") as file:
                notefamily_text = noteFamily + " ->\n" + return_noteFamily(noteFamily)
                file.write(notefamily_text)

            os.startfile(note_file)

    # =====================================================
    # EXIT
    # =====================================================

    elif "exit" in cmd:
        sayywrite("Are you sure?")
        confirm = listen()

        if confirm and "yes" in confirm.lower():
            sayywrite("Goodbye!")
            break
        else:
            sayywrite("Cancelled.")
