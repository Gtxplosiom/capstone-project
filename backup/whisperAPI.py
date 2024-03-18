import whisper
import threading
import click_on_screen

import openThings

tiny_model = whisper.load_model('models/tiny.en.pt')
base_model = whisper.load_model('models/base.en.pt')

output = ""

def OpenApp(App):
    if App == "Browser":
        open("google chrome")
    elif App == "Notes" or App == "Notepad" or App == "Note":
        open("notepad")

def Punctuation(string):
 
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
 
    for x in string.lower():
        if x in punctuations:
            string = string.replace(x, "")
    
    return string

def Whisper_Recognition():
    import speech_recognition as sr
    import tempfile
    import os
    import re

    def continuous_listen():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=5)
            recognizer.energy_threshold = 4000
            recognizer.dynamic_energy_threshold = True

        try:
            while True:
                with microphone as source:
                    print("listening...")
                    try:
                        audio = recognizer.listen(source, timeout=5)

                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        result = base_model.transcribe(temp_audio_path)
                        prompt_text = result['text']
                        prompt_text = Punctuation(prompt_text)
                        prompt_text = prompt_text.lower()

                        split_result = prompt_text[1:].split(" ")
                        keyword = split_result[0].capitalize()

                        print(f"You said: {prompt_text}")
                        print(split_result)

                        if keyword == "Click":
                            if len(split_result) > 1:
                                command = split_result[1].capitalize()
                                print(command)
                                click_on_screen.Click(command)
                            else:
                                click_on_screen.pyautogui.click()
                        if keyword == "Open":
                            if len(split_result) > 1:
                                command = split_result[1].capitalize()
                                print(command)
                                openThings.open(command)
                            else:
                                click_on_screen.DoubleClick()
                        elif keyword == "Close":
                            if len(split_result) > 1:
                                command = split_result[1].capitalize()
                                print(command)
                                openThings.close(command)
                            else:
                                pass


                        os.remove(temp_audio_path)

                    except sr.WaitTimeoutError:
                        print("Listening timed out. No audio detected.")
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Error with the API request; {e}")

        except KeyboardInterrupt:
            print("Stopping the continuous listening.")

    continuous_listen()

Whisper_Recognition()
