import pygetwindow as gw
import time
from vosk import Model, KaldiRecognizer
import pyaudio

from win11toast import toast

model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)

def ActiveWindow():
    return gw.getActiveWindow().title if gw.getActiveWindow() else None

def Notepad():
    toggle = True
    toast('Currently Using: Notepad')
    while toggle == True:
        active_window = ActiveWindow()
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            print("Hello I'm Notepad")
            time.sleep(1)
            if 'Notepad' not in str(active_window):
                toggle = False

            # text = recognizer.Result()
            # trimmedText = text[14:-3]

            # splitText = trimmedText.split(" ")

            # keyword = splitText[0].capitalize()
                
def Word():
    toggle = True
    toast('Currently Using: Microsoft Word')
    while toggle == True:
        active_window = ActiveWindow()
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            print("Hello I'm Microsoft Word")
            time.sleep(1)
            if 'Word' not in str(active_window):
                toggle = False

def Focused(): # can be removed??
    prevActiveWin = None

    while True:
        currActiveWin = ActiveWindow()

        if currActiveWin != prevActiveWin:
            print("Active Window:", currActiveWin)
            prevActiveWin = currActiveWin

        time.sleep(1)
