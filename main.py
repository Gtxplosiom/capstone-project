import threading
import UI
import voiceRecognition
import FocusApp
import keyboard, os

def task1():
    UI.startUI()

def task2():
    voiceRecognition.voiceRecog()

def task3():
    FocusApp.Focused()

thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)
thread3 = threading.Thread(target=task3, daemon=True)

thread1.start()
thread2.start()
thread3.start()

keyboard.add_hotkey('esc', lambda: os._exit(1))