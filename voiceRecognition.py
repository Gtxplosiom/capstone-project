from vosk import Model, KaldiRecognizer

import pyaudio

import threading
import time

import clickOnScreen
import cameraMouse

activateMouse = True

pause = threading.Event()

def voiceRecog():
    model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
    recognizer = KaldiRecognizer(model, 16000)

    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            trimmedText = text[14:-3]

            splitText = trimmedText.split(" ")

            keyword = splitText[0].capitalize()
            print(keyword)
            print(trimmedText)

            if trimmedText == "open mouse":
                global activateMouse
                activateMouse = True
                thread1 = threading.Thread(target=cameraMouse.camera_mouse)
                thread1.start()
            elif trimmedText == "close mouse":
                activateMouse = False

            # commands
            if keyword == "Click":
                if len(splitText) > 1:
                    command = splitText[1].capitalize()
                    print(command)
                    clickOnScreen.click(command)
                else:
                    clickOnScreen.pyautogui.click()
            elif keyword == "Double" and splitText[1].capitalize() == "Click":
                if len(splitText) > 1:
                    command = splitText[2].capitalize()
                    print(command)
                    clickOnScreen.doubleClick(command)
                else:
                    clickOnScreen.pyautogui.doubleClick()
            elif keyword == "Look":
                if len(splitText) > 1:
                    command = splitText[1].capitalize()
                    print(command)
                    clickOnScreen.highlightTk(command)
                else:
                    print("What to find?")
            elif keyword == "Cancel":
                print("Cancelled")
            elif keyword == "Hover":
                command = splitText[1].capitalize()
                print(command)
                clickOnScreen.hover(command)
            elif keyword == "Type":
                voiceType()
            else:
                print("Waiting for a command")

            def voiceType():
                toggle = True
                while toggle == True:
                    data = stream.read(4096, exception_on_overflow=False)
                    if recognizer.AcceptWaveform(data):
                        text = recognizer.Result()
                        trimmedText = text[14:-3]

                        splitText = trimmedText.split(" ")

                        keyword = splitText[0].capitalize()

                        if keyword == "Stop":
                                toggle = False
                                break
                        elif keyword == "Clear":
                            clickOnScreen.pyautogui.press('backspace')
                        else:
                            if len(keyword) == 0:
                                print("Say something")
                            else:
                                for i in range(len(splitText)):
                                    transcribedText = [firsts[0] if firsts != "space" else "space" for firsts in splitText]
                                    result = ''.join(transcribedText)
                                result = result.replace("space", " ")
                                print(splitText)
                                print(result)
                                clickOnScreen.pyautogui.typewrite(result)
                                transcribedText.clear()