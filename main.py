import threading
import speechRecognition
import requests
import keyboard
import os

def ASR():
    print("Starting ASR...")
    speechRecognition.Whisper_Recognition()

def internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False    

if __name__ == "__main__":
    if internet_connection():
        print("The Internet is connected.")
        thread1 = threading.Thread(target=ASR)
        thread1.start()

    else:
        print("The Internet is not connected.")
        thread1 = threading.Thread(target=ASR)
        thread1.start()

    keyboard.add_hotkey('esc', lambda: os._exit(1))