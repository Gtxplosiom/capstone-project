import pygetwindow as gw
import time
from vosk import Model, KaldiRecognizer
import pyaudio

import threading

import pyautogui
import cameraMouse

from win11toast import toast

from AppOpener import open, close

model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)

activate_mouse = True

def TrimString(input_string, keywords):
    words = input_string.split()

    for keyword in keywords:
        try:
            index_of_keyword = words.index(keyword)
            trimmed_string = ' '.join(words[index_of_keyword:])
            return trimmed_string
        except ValueError:
            continue  # Try the next keyword if the current one is not found

    # None of the keywords were found in the string
    return input_string

def ActiveWindow():
    return gw.getActiveWindow().title if gw.getActiveWindow() else None

def MouseScroll():
    screen_width, screen_height = pyautogui.size()

    x_coordinate = screen_width - 1  # Rightmost side
    y_coordinate = screen_height // 2  # Center vertically

    pyautogui.moveTo(x_coordinate, y_coordinate)

def Toast(App):
    toast(f'Currently Using: {App}', 'wait for sound for commands to be available...')

def Notepad():
    toggle = True
    Toast("Notepad")
    while toggle == True:
        active_window = ActiveWindow()
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            print("Hello I'm Notepad")
            time.sleep(1)
            if 'Notepad' not in str(active_window):
                toggle = False
                
def Word():
    toggle = True
    Toast("Microsoft Word")
    while toggle == True:
        active_window = ActiveWindow()
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            print("Hello I'm Microsoft Word")
            time.sleep(1)
            if 'Word' not in str(active_window):
                toggle = False

def Chrome():
    chrome_toggle = True
    Toast("Google Chrome")

    while chrome_toggle == True:
        active_window = ActiveWindow()
        
        
        if 'Chrome' not in str(active_window):
            chrome_toggle = False

def Focused():
    prevActiveWin = None

    while True:
        currActiveWin = ActiveWindow()

        if currActiveWin != prevActiveWin:
            print("Active Window:", currActiveWin)
            prevActiveWin = currActiveWin

        time.sleep(1)
