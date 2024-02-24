import threading
import ui
import voiceRecognition
import focusApp
import keyboard
import os

def StartUI():
    ui.StartUI()

def VoiceRecognition():
    voiceRecognition.VoiceRecog()

def FocusedApp():
    focusApp.Focused()

if __name__ == "__main__":
    thread1 = threading.Thread(target=StartUI)
    thread2 = threading.Thread(target=VoiceRecognition)
    thread3 = threading.Thread(target=FocusedApp, daemon=True)

    thread1.start()
    thread2.start()
    thread3.start()

    keyboard.add_hotkey('esc', lambda: os._exit(1))