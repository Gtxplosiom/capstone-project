import cameraMouse
import threading
import subprocess

activate_mouse = False
tutorial_active = False

def open(things):
    print(f"Opening {things}...")
    if things == "Mouse":
        global activate_mouse
        activate_mouse = True
        thread1 = threading.Thread(target=cameraMouse.CameraMouse)
        thread1.start()
    if things == "Tutorial":
        from tutorial import Tutorial

        global tutorial_active
        tutorial_active = True
        
        tutorial = Tutorial()

        thread_tutorial = threading.Thread(target=tutorial.run)
        thread_tutorial.start()
    else:
        if things == "Browser":
            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        elif things == "Notes" or things == "Notepad" or things == "Note":
            subprocess.Popen("notepad.exe")

def close(things):
    print(f"Closing {things}...")
    if things == "Mouse":
        global activate_mouse
        activate_mouse = False
    else:
        if things == "Browser":
            close("google chrome")
        elif things == "Notes" or things == "Notepad" or things == "Note":
            close("notepad")

class OpenClose:
    def __init__(self):
        pass