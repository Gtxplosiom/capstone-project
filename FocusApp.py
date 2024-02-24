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
    toggle = True
    Toast("Google Chrome")

    # keywords for command (Chrome) to "keyword spot" the keywords in between sentences
    keywords = ["search", "new", "find", "scroll", "write", "right", "enter", "up", "down", "maximize", "maximise", "click"]

    while toggle == True:
        active_window = ActiveWindow()
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            trimmed_text = text[14:-3]

            print("running")

            result = TrimString(trimmed_text, keywords)

            split_result = result.split(" ")

            keyword = split_result[0].capitalize()

            print(result)

            string = split_result[1:]
            string = ' '.join(split_result[1:]).replace("[", "").replace("]", "").replace(",", "")

            # camera mouse
            if result == "open mouse" or result == "open mouth" or result == "open most":
                global activate_mouse
                activate_mouse = True
                thread1 = threading.Thread(target=cameraMouse.CameraMouse)
                thread1.start()
            elif result == "close mouse" or result == "close mouth" or result == "close most":
                activate_mouse = False

            # commands block
            if keyword == "Search":
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(0.1)
                pyautogui.hotkey('backspace')
            elif keyword == "Write" or keyword == "Right":
                pyautogui.typewrite(str(string))
            elif keyword == "Enter":
                pyautogui.hotkey('enter')
            elif keyword == "Up":
                pyautogui.hotkey('up')
            elif keyword == "Down":
                pyautogui.hotkey('down')
            elif "new tab" in result:
                pyautogui.hotkey('ctrl', 't')
            elif "close tab" in result:
                pyautogui.hotkey('ctrl', 'w')
            elif "scroll down" in result:
                MouseScroll()
                pyautogui.scroll(-1000)
            elif "scroll up" in result:
                MouseScroll()
                pyautogui.scroll(1000)
            elif keyword == "Maximize" or keyword == "Maximise":
                pyautogui.hotkey('alt', 'space')
                time.sleep(0.1)
                pyautogui.hotkey('x')
            elif keyword == "Click":
                pyautogui.click()
            elif "close browser" in result:
                close("google chrome")
            else:
                pass
        if 'Chrome' not in str(active_window):
            toggle = False

def Focused():
    prevActiveWin = None

    while True:
        currActiveWin = ActiveWindow()

        if currActiveWin != prevActiveWin:
            print("Active Window:", currActiveWin)
            prevActiveWin = currActiveWin

        time.sleep(1)
