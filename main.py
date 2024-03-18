import threading
import requests
import keyboard
import os

def ASR():
    print("Starting ASR...")

if __name__ == "__main__":
    thread1 = threading.Thread(target=ASR)
    thread1.start()

    keyboard.add_hotkey('esc', lambda: os._exit(1))