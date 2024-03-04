from vosk import Model, KaldiRecognizer

import pyaudio

import threading
import time

import clickOnScreen
import cameraMouse
import focusApp

from AppOpener import open

activate_mouse = True

pause = threading.Event()

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


def VoiceRecog():
    model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
    stream.start_stream()

    # keywords for command (for keyword matching in between sentences)
    keywords = ["click", "double", "look", "open"]

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        notepad_window = focusApp.gw.getWindowsWithTitle('Notepad') # test
        active_window = str(focusApp.gw.getActiveWindow())

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            trimmed_text = text[14:-3]
            
            print("running")

            result = TrimString(trimmed_text, keywords)

            split_result = result.split(" ")

            keyword = split_result[0].capitalize()

            print(result)

            if "open mouse" in result:
                global activate_mouse
                activate_mouse = True
                thread1 = threading.Thread(target=cameraMouse.CameraMouse)
                thread1.start()
            elif "close mouse" in result:
                activate_mouse = False

            # commands
            if keyword == "Click":
                if len(split_result) > 1:
                    command = split_result[1].capitalize()
                    print(command)
                    clickOnScreen.Click(command)
                else:
                    clickOnScreen.pyautogui.click()
            elif keyword == "Double" and split_result[1].capitalize() == "Click":
                if len(split_result) > 1:
                    command = split_result[1].capitalize()
                    print(command)
                    clickOnScreen.DoubleClick(command)
                else:
                    clickOnScreen.pyautogui.doubleClick()
            elif keyword == "Open":
                if len(split_result) > 1:
                    command = split_result[1].capitalize()
                    print(command)
                    OpenApp(command)
                else:
                    pass
            elif keyword == "Look":
                if len(split_result) > 1:
                    command = split_result[1].capitalize()
                    print(command)
                    clickOnScreen.HighlightTk(command)
                else:
                    print("What to find?")
            elif keyword == "Cancel":
                print("Cancelled")
            elif keyword == "Hover":
                command = split_result[1].capitalize()
                print(command)
                clickOnScreen.hover(command)
            elif keyword == "Type":
                VoiceType()

            # Active window
            elif 'Notepad' in active_window: # test (can be moved to another file)
                focusApp.Notepad()
            elif 'Word' in active_window: # test (can be moved to another file)
                focusApp.Word()
            elif 'Chrome' in active_window: # test (can be moved to another file)
                focusApp.Chrome()

            else:
                print("Waiting for a command")

            def VoiceType():
                toggle = True
                while toggle == True:
                    data = stream.read(4096, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        text = recognizer.Result()
                        trimmed_text = text[14:-3]

                        split_text = trimmed_text.split(" ")

                        keyword = split_text[0].capitalize()

                        if keyword == "Stop":
                                toggle = False
                                break
                        elif keyword == "Clear":
                            clickOnScreen.pyautogui.press('backspace')
                        else:
                            if len(keyword) == 0:
                                print("Say something")
                            else:
                                for i in range(len(split_text)):
                                    transcribed_text = [firsts[0] if firsts != "space" else "space" for firsts in split_text]
                                    result = ''.join(transcribed_text)
                                result = result.replace("space", " ")
                                print(split_text)
                                print(result)
                                clickOnScreen.pyautogui.typewrite(result)
                                transcribed_text.clear()
            def OpenApp(App):
                if App == "Browser":
                    open("google chrome")
                elif App == "Notes" or App == "Notepad" or App == "Note":
                    open("notepad")