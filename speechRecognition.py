import speech_recognition as sr
import tempfile
import os
import whisper
import pygetwindow as gw

import clickOnScreen
import focusApp
import openThings
import clickOnScreen

import threading

class SpeechRecognitionWhisper:
    asr_active = False
    def __init__(self):
        ## speech recognition variables
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.recognizer.pause_threshold = 0.5
        self.tiny_model = whisper.load_model('models/tiny.en.pt')
        self.base_model = whisper.load_model('models/base.en.pt')

        ## other variables
        self.punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

        self.asr_active = True

    @staticmethod
    def ActiveWindow():
        return gw.getActiveWindow().title if gw.getActiveWindow() else None

    def Punctuation(self, string: str):
        for x in string.lower():
            if x in self.punctuations:
                string = string.replace(x, "")
        return string
    
    def Listening(self):
        with self.microphone as self.source:
            self.recognizer.energy_threshold = 200
            self.recognizer.dynamic_energy_threshold = False

            print("Listening...")
            while True:
                active_window = self.ActiveWindow()
                if 'Chrome' in str(active_window):

                    print("Using Google Chrome")
                    try:
                        audio = self.recognizer.listen(self.source, timeout=5)

                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        result = self.base_model.transcribe(temp_audio_path)
                        prompt_text = result['text']
                        prompt_text = self.Punctuation(prompt_text)
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
                        audio = self.recognizer.listen(self.source, timeout=5)

                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        result = self.base_model.transcribe(temp_audio_path)
                        prompt_text = result['text']
                        prompt_text = self.Punctuation(prompt_text)
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
                        audio = self.recognizer.listen(self.source, timeout=5)

                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        result = self.base_model.transcribe(temp_audio_path)
                        prompt_text = result['text']
                        prompt_text = self.Punctuation(prompt_text)
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

asr = SpeechRecognitionWhisper()

asr.Listening()