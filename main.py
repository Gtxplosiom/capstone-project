import threading
import UI
import voiceRecognition
import cameraMouse
import keyboard, os

def task1():
    UI.startUI()

def task2():
    voiceRecognition.voiceRecog()

# Create processes
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)

# Start processes
thread1.start()
thread2.start()

# End Application
keyboard.add_hotkey('esc', lambda: os._exit(1))

# Wait for processes to finish
# thread1.join()
# thread2.join()