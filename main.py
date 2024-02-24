import threading
import ui
import voiceRecognitionOffline
import voiceRecognitionOnline
import focusApp
import requests
import keyboard
import os

def StartUI():
    ui.StartUI()

def VoiceRecognitionOffline():
    voiceRecognitionOffline.VoiceRecog()

def VoiceRecognitionOnline():
    voiceRecognitionOnline.VoiceRecog()

def FocusedApp():
    focusApp.Focused()

def internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False    

if __name__ == "__main__":
    if internet_connection():
        print("The Internet is connected.")
        thread1 = threading.Thread(target=StartUI)
        thread2 = threading.Thread(target=VoiceRecognitionOffline)
        thread2_5 = threading.Thread()
        thread3 = threading.Thread(target=FocusedApp, daemon=True)
        thread1.start()
        thread2.start()
        thread3.start()
    else:
        print("The Internet is not connected.")
        thread1 = threading.Thread(target=StartUI)
        thread2 = threading.Thread(target=VoiceRecognitionOffline)
        thread2_5 = threading.Thread()
        thread3 = threading.Thread(target=FocusedApp, daemon=True)
        thread1.start()
        thread2.start()
        thread3.start()

    keyboard.add_hotkey('esc', lambda: os._exit(1))