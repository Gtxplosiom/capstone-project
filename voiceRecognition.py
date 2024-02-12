from vosk import Model, KaldiRecognizer

import pyaudio

import clickOnScreen

model = Model(r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\models\vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

file_path = 'commands.txt'

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
        
        if keyword == "Click":
            command = splitText[1].capitalize()
            clickOnScreen.Click(command)
        elif keyword == "Double" and splitText[1].capitalize() == "Click":
            command = splitText[2].capitalize()
            clickOnScreen.doubleClick(command)
        else:
            print("Waiting for a command")

        # print(keyword[0].capitalize())
        # print(trimmedText.capitalize())
        # clickOnScreen.Click(trimmedText.capitalize())
        