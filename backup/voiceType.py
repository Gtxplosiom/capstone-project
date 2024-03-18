from vosk import Model, KaldiRecognizer

import pyaudio

import keyboard
import time

import click_on_screen

model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

mic = pyaudio.PyAudio()

stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        if recognizer.FinalResult():
            trimmed_text = text[14:-3]

            split_text = trimmed_text.split(" ")

            keyword = split_text[0].capitalize()

            if keyword == "Stop":
                    toggle = False
                    break
            elif keyword == "Clear":
                click_on_screen.pyautogui.press('backspace')
            elif len(keyword) == 0:
                    print("Say something")
            else:
                for i in range(len(split_text)):
                    transcribed_text = [firsts[0] if firsts != "space" else "space" for firsts in split_text]
                    result = ''.join(transcribed_text)
                if "space" in result:
                    result = result.replace("space", " ")
                print(split_text)
                print(result)
                if len(split_text) > 0:
                    keyboard.write(result)
                    time.sleep(1)
                else:
                    time.sleep(1)