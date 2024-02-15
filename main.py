import threading
import UI
import voiceRecognition
import cameraMouse
import keyboard, os

def task1():
    UI.startUI()

def task2():
    voiceRecognition.voiceRecog()

thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)

thread1.start()
thread2.start()

keyboard.add_hotkey('esc', lambda: os._exit(1))