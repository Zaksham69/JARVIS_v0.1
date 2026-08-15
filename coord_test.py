import pyautogui
import json
import time

raw_test_subject = input("Which coordinate do you want to check: ").upper()
test_subject = raw_test_subject.replace(' ', '_')
with open("coords.json", "r") as file:
    data = json.load(file)
    print("going to coordinates in")
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    time.sleep(1)
    pyautogui.moveTo(*test_subject)
    