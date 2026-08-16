
import pyautogui
import datetime
import time as _Time
import wikipedia
import os
import subprocess
import webbrowser
from functions import *
import hashlib


# =========================================================
# MAIN LOOP
# =========================================================
with open("password.txt", "r") as file:
    content = file.read()
    i = content.find[', ']
    times_open = content[:i]
    
home_screen()

if times_open != 0:
    times_open = times_open+1

while True:
    cmd = listen()
    if times_open == 0:
        with open("password.txt", "w+") as file:
            password = ask_field("Enter your PC password for confirmations like shutdown")
            if password is None:
                sayywrite("Sorry I didn't catch that")
                continue
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            file.write(f"{times_open+1}, {hashed_password}")
    with open("password.txt", "w") as file:
        file.write(f"{times_open+1}, {hashed_password}")

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
    # OPEN
    # =====================================================

    if cmd.startswith("open"):
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
                subprocess.Popen([
                    "explorer.exe",
                    f"shell:AppsFolder\\{value}"
                ])

            # Normal executable
            elif isinstance(value, str):
                os.startfile(value)

        else:
            dot_index = -1
        
            for i in range(len(app)):
                if app[i] == '.':
                    dot_index = i
                    break
        
            if dot_index != -1:
                if dot_index <= 3:
                    if '.' in app[dot_index + 1:]:
                        webbrowser.open(f"https://{app.lower()}")
                    else:
                        webbrowser.open(f"https://{app.lower()}.com")
                else:
                    webbrowser.open(f"https://{app.lower()}")
            else:
                webbrowser.open(f"https://www.{app.lower()}.com")

    # =====================================================
    # MINECRAFT
    # =====================================================

    elif "minecraft" in cmd:
        sayywrite("Opening Minecraft")

        try:
            os.startfile(APPS["TLAUNCHER"])
        except KeyError:
            sayywrite("TLauncher is not configured in apps.json.")
            continue

        _Time.sleep(45)

        move(*COORDS["MINECRAFT"])
        pyautogui.click()

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
            subprocess.Popen(APPS["CHROME"])

        except KeyError:
            sayywrite("Chrome is not configured in apps.json.")
            continue

        _Time.sleep(2)

        move(*COORDS["CHROME_SEARCH_BOX"])
        pyautogui.click()

        write(query)
        pyautogui.press("enter")

    # =====================================================
    # SHUTDOWN
    # =====================================================

    elif "shutdown" in cmd:
        confirm = ask_field("Password")

        if confirm and password in confirm:
            pyautogui.hotkey("win", "x")
            pyautogui.press("u")
            pyautogui.press("u")

        else:
            sayywrite("Cancelled")

    # =====================================================
    # ADD CONTACT
    # =====================================================

    elif "add contact" in cmd:
        try:
            parts = (
                cmd.replace("add contact", "", 1)
                .strip()
                .split(" as ")
            )

            nickname = parts[0].strip()
            name = parts[1].strip()
            if nickname == "written":
                nickname = input("Contact: ")

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

        # -------------------------------------------------
        # EMAIL
        # -------------------------------------------------

        email = ask_field("Email")

        if email is None:
            sayywrite("Client was not added.")
            continue

        # -------------------------------------------------
        # PHONE / WHATSAPP
        # -------------------------------------------------

        number = ask_field("Phone number/Whatsapp number (if any)")

        phone = ""
        whatsapp = ""

        if number:
            number = number.strip()

            # Example:
            # 9876543210/9876543211
            # Phone / WhatsApp

            if "/" in number:
                i = number.find("/")

                phone = number[:i].strip()
                whatsapp = number[i + 1:].strip()

            # Only one number
            else:
                phone = number
            destination = ""

        # -------------------------------------------------
        # NOTES
        # -------------------------------------------------

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

        # -------------------------------------------------
        # SAVE CLIENT
        # -------------------------------------------------

        clients[client] = {
            "Email": email,
            "Phone": phone,
            "Whatsapp": whatsapp,
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

        # Match field names regardless of capitalization.
        field_map = {
            "email": "Email",
            "phone": "Phone",
            "whatsapp": "Whatsapp",
            "destination": "Destination",
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

        # Notes should remain a list.
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

        # -------------------------------------------------
        # ALL FIELDS
        # -------------------------------------------------

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

        # -------------------------------------------------
        # EMAIL
        # -------------------------------------------------

        elif field == "email":
            sayywrite(clients[client]["Email"])

        # -------------------------------------------------
        # PHONE
        # -------------------------------------------------

        elif field == "phone" or "phone" in field:
            sayywrite(clients[client]["Phone"])

        # -------------------------------------------------
        # WHATSAPP
        # -------------------------------------------------

        elif field == "whatsapp" or "whatsapp" in field:
            sayywrite(clients[client]["Whatsapp"])

        # -------------------------------------------------
        # PASSPORT
        # -------------------------------------------------

        elif field == "passport":
            sayywrite(clients[client]["Passport"])

        # -------------------------------------------------
        # DESTINATION
        # -------------------------------------------------

        elif field == "destination":
            sayywrite(clients[client]["Destination"])

        # -------------------------------------------------
        # VISA
        # -------------------------------------------------

        elif field == "visa":
            sayywrite(clients[client]["Visa"])

        # -------------------------------------------------
        # NOTES
        # -------------------------------------------------

        elif field == "notes":
            sayywrite(str(clients[client]["Notes"]))

        # -------------------------------------------------
        # INVALID FIELD
        # -------------------------------------------------

        else:
            sayywrite("The field doesn't exist.")

    # =====================================================
    # SEARCH FIELD
    # =====================================================

    elif "search field" in cmd:
        clients = load_clients()

        field = cmd.replace("search field ", "").strip()
        value = ask_field("Value?")

        client_list = list(clients.items())

        for i in range(len(client_list)):
            client = client_list[i][1]

            if client.get(field) == value:
                break
            else:
                client = None

        if client is None:
            sayywrite("Client not detected")
        else:
            sayywrite(client)

    # =====================================================
    # NOTES 
    # =====================================================
    
    elif "add note family" in cmd:
        noteFamily = cmd.replace("add note family ", "").strip()
        notes = load_notes()
        if noteFamily in notes:
            sayywrite("Note family already exists, would you like me to replace it?")
            replaceYN = listen()
            if replaceYN.lower() == "yes":
                notes[noteFamily] = []
            elif replaceYN is None:
                sayywrite("Sorry I didn't catch that.")
                continue
            else:
                continue
            
        notes[noteFamily] = []
        sayywrite("Note family added, would you like to enter your first note in it?")
        confirm_note = listen()
        if confirm_note is None:
            sayywrite("Sorry I didn't catch that.")
            continue
        elif confirm_note.lower() == "yes":
            sayywrite(f"What is your first note in {noteFamily}")
            note = listen()
            if note is None:
                sayywrite("Sorry I didn't catch that.")
                continue
            notes[noteFamily].append(note)
            
        save_notes(notes)
     
    elif "add note" in cmd :
        notes = load_notes()
        query = cmd.replace("add note ", "").strip()
        if "in note family" in cmd:            
            i = query.find(" in note family ")
            note = query[:i]
            noteFamily = query[i+len(" in note family ")-1:]
        else:
            note = query
            noteFamily = ask_field("Note family?")  
            if noteFamily is None:
                sayywrite("Sorry, I didn't catch that.")
                continue 
        if noteFamily not in notes:
            sayywrite("Note family does not exist.")
            continue
        elif note in notes[noteFamily]:
            sayywrite("Note already exists, do you want me to replace it?")
            confirm = listen()
            if confirm is None:
                sayywrite("Sorry, I didn't catch that.")
                continue
            elif confirm.lower() == "yes" or "yes" in confirm.lower():
                sayywrite("Thanks for the confirmation.")
                notes[noteFamily].remove(notes)
            else:
                sayywrite("That would be taken as a no")
                continue
        
        notes[noteFamily].append(note)                                          
        
    elif "show note family" in cmd:
        notes = load_notes
        noteFamily = cmd.replace("show note family ", "").strip()
        if noteFamily not in notes:
            sayywrite("Note family does not exist.")
            continue
        print_noteFamily(noteFamily)
        sayywrite("Note Family printed, would you like to recite it for you? Or perhaps show it in a file?")
        show = listen()
        if show is None:
            sayywrite("Sorry I didn't catch that." )
            continue
        elif "recite" in show.lower():
            sayywrite(notes[noteFamily])
        elif "file" in show.lower():
            with open("noteFamily.txt", "w")as file:
                notefamily = noteFamily+'->\n'+return_noteFamily(noteFamily)
                file.write(notefamily)
            os.startfile(SCRIPT_DIR/"noteFamily")
    # =====================================================
    # EXIT
    # =====================================================

    elif "exit" in cmd:
        sayywrite("Are you sure?")
        sayywrite("Goodbye!")
        break

