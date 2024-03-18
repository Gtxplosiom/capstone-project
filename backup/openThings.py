import threading
import subprocess

class OpenClose:
    def __init__(self):

        self.activate_mouse = False
        self.tutorial_active = False

    def open(self, things):
        
        if things == "Mouse":
            import camera_mouse

            print(f"Opening {things}...")

            self.activate_mouse = True

            thread1 = threading.Thread(target=camera_mouse.CameraMouse)
            thread1.start()

        elif things == "Browser":
            print(f"Opening {things}...")

            subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        elif things == "Notes" or things == "Notepad" or things == "Note":
            print(f"Opening {things}...")

            subprocess.Popen("notepad.exe")

    def close(self, things):
        print(f"Closing {things}...")

        if things == "Mouse":
            self.activate_mouse = False

        else:
            if things == "Browser":
                self.close("google chrome")
            elif things == "Notes" or things == "Notepad" or things == "Note":
                self.close("notepad")