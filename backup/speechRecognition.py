import whisper
import pygetwindow as gw

import clickOnScreen
import focusApp
import openThings
import clickOnScreen


import threading

tiny_model = whisper.load_model('models/tiny.en.pt')
base_model = whisper.load_model('models/base.en.pt')

output = ""
asr_active = False

def ActiveWindow():
    return gw.getActiveWindow().title if gw.getActiveWindow() else None

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

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    recognizer.pause_threshold = 0.5
    global asr_active
    asr_active = True

    with microphone as source:
        recognizer.energy_threshold = 200
        recognizer.dynamic_energy_threshold = False
        print("listening...")
        active_window = ActiveWindow()
        while True:
            active_window = ActiveWindow()
            if 'Chrome' in str(active_window):
                print("Using Google Chrome")
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

                    # print(f"You said: {prompt_text}")
                    # print(split_result)

                    focusApp.Chrome(prompt_text)
                    
                        
                    os.remove(temp_audio_path)

                except sr.WaitTimeoutError:
                    print("Listening timed out. No audio detected.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Error with the API request; {e}")
            elif openThings.tutorial_active:
                print("In Tutorial")
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

                    # print(f"You said: {prompt_text}")
                    # print(split_result)

                    focusApp.Guide(prompt_text)
                    
                        
                    os.remove(temp_audio_path)

                except sr.WaitTimeoutError:
                    print("Listening timed out. No audio detected.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Error with the API request; {e}")
            else:
                print("Not using specified programs")
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

                    ## commands here
                    if keyword == "Click":
                        if len(split_result) > 1:
                            command = split_result[1].capitalize()
                            print(command)
                            clickOnScreen.HighlightTk(command)
                        else:
                            clickOnScreen.pyautogui.click()
                    if keyword == "Open":
                        if len(split_result) > 1:
                            command = split_result[1].capitalize()
                            print(command)
                            openThings.open(command)
                        else:
                            clickOnScreen.DoubleClick()
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