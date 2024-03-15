import os
import time
import keyboard
import tkinter as tk
import speech_recognition as sr
import whisper
from threading import Thread
from PIL import Image, ImageTk

class WhisperASR:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = script_dir.replace('\\', '/')
    tiny_model_path = os.path.expanduser(f'{script_dir}/models/tiny.en.pt')

    is_listening = False
    def __init__(self, window_asr):
        self.window_asr = window_asr

        # tiny_model_path = os.path.expanduser('D:/Capstone/Capstone-Application/models/tiny.en.pt')

        self.model = whisper.load_model(self.tiny_model_path)
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()

    def check_listen(self, listening):
        time.sleep(0.1)
        self.window_asr.update_state(listening)

    def whisper_sr(self, audio):
        result = self.model.transcribe(audio)
        text = result['text']
        return text

    def recognize_speech(self):
        while True:
            with self.mic as source:
                self.is_listening = True
                self.check_listen(self.is_listening)
                try:
                    self.recognizer.adjust_for_ambient_noise(source)

                    audio = self.recognizer.listen(source, timeout=5)

                    self.is_listening = False
                    self.check_listen(self.is_listening)

                    with open('speech.wav', 'wb') as f:
                        f.write(audio.get_wav_data())
                    
                    text = self.whisper_sr('speech.wav')

                    self.window_asr.show_result(text)

                    os.remove('speech.wav')

                except sr.UnknownValueError:
                    self.window_asr.show_result("Whisper Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    self.window_asr.show_result("Could not request results from Whisper Speech Recognition; {0}".format(e))
                except sr.WaitTimeoutError:
                    self.window_asr.show_result("Listening timed out. No audio detected.")

class WindowASR:
    def __init__(self, root):
        self.root = root
        self.root.title("Sample App")
        self.root.geometry("400x200+1500+700")

        self.state_label = tk.Label(self.root, text="checking state...")
        self.state_label.pack(pady=20)

        self.result_label = tk.Label(self.root, text="waiting for result...")
        self.result_label.pack(pady=20)

        self.app_asr = WhisperASR(self)

        thread_asr = Thread(target=self.app_asr.recognize_speech)
        thread_asr.start()

        thread_check = Thread(target=lambda: self.app_asr.check_listen(WhisperASR.is_listening))
        thread_check.start()

    def exit_program(self, e):
        if e.name == 'esc':
            os._exit(0)

    def update_state(self, listening):
        if listening:
            self.state_label.configure(text="Listening...")
        else:
            self.state_label.configure(text="Processing audio...")

    def show_result(self, result):
        self.result_label.configure(text=result)
        self.result_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app_window = WindowASR(root)

    keyboard.on_press(app_window.exit_program)

    root.mainloop()