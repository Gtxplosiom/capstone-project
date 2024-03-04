import cameraMouse
import tutorial
import threading
import subprocess

activate_mouse = False

def open(things):
    print(f"Opening {things}...")
    if things == "Mouse":
        global activate_mouse
        activate_mouse = True
        thread1 = threading.Thread(target=cameraMouse.CameraMouse)
        thread1.start()
    elif things == "Tutorial":
        tutorial.activate_tsr = True
        thread2 = threading.Thread(target=tutorial.Tutorial)
        thread2.start()
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