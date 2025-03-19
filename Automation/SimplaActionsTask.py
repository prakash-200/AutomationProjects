import pyautogui
import time

def open_notepad_and_type():
    # Open the Start menu (Windows key) and type 'notepad'
    pyautogui.press('winleft')
    time.sleep(1)
    pyautogui.write('notepad')
    time.sleep(1)
    pyautogui.press('enter')

    # Wait for Notepad to open
    time.sleep(2)

    # Type a message in Notepad
    pyautogui.write('Hello, this is an automated message!', interval=0.1)
    print("Task completed!")

# Run the automation
open_notepad_and_type()