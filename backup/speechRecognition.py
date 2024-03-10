import whisper
import pygetwindow as gw

# import clickOnScreen
# import focusApp
# # import openThings


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
        print(recognizer.energy_threshold)
        # recognizer.dynamic_energy_threshold = False
        print("listening...")
        active_window = ActiveWindow()
        while True:
            active_window = ActiveWindow()
            print("Not using specified programs")
            try:
                recognizer.adjust_for_ambient_noise(source)
                print(recognizer.energy_threshold)
                audio = recognizer.listen(source)
                audio.get_wav_data()

                with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                    temp_audio_path = temp_audio.name
                    temp_audio.write(audio.get_wav_data())

                result = base_model.transcribe(audio)
                prompt_text = result['text']
                prompt_text = Punctuation(prompt_text)
                prompt_text = prompt_text.lower()

                split_result = prompt_text[1:].split(" ")
                keyword = split_result[0].capitalize()

                print(f"You said: {prompt_text}")
                print(split_result)

                os.remove(temp_audio_path)

            except sr.WaitTimeoutError:
                print("Listening timed out. No audio detected.")
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Error with the API request; {e}")

Whisper_Recognition()