import tkinter as tk
from threading import Thread
import os
import whisper
import speech_recognition as sr

import cv2
import dlib
import pyautogui as screen

class TutorialSR:
    def __init__(self, tutorial):
        self.tutorial = tutorial
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.tiny_model = whisper.load_model('models/tiny.en.pt')
        self.base_model = whisper.load_model('models/base.en.pt')

        self.in_tutorial = True

        self.mouse = CameraMouse()

    def audio_to_wav(self, audio):
        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    def transcribe_to_text(self, model):
        result = model.transcribe('speech.wav')

        text = result['text']
        text = text.lower()
        text = text.split(' ')
        text.remove(text[0])

        return text

    def sr_tutorial(self):
        while self.in_tutorial:
            with self.mic as source:
                print("In tutorial")
                self.r.adjust_for_ambient_noise(source)

                try:
                    audio = self.r.listen(source)
                    self.audio_to_wav(audio)

                    text = self.transcribe_to_text(self.base_model)
                    if len(text) > 0:
                        command = text[0]
                        print(command)

                        if command == "next" or command == "next.":
                            self.tutorial.next_part()
                        elif command == "open" or command == "open.":
                            if len(text) > 1:
                                command2 = text[1]
                                if command2 == "mouse" or command2 == "mouse.":
                                    self.tutorial.add_text("Opening mouse. Wait for a sec...")
                                    self.tutorial.add_text("Say 'Next' to proceed.")
                                    thread_mouse = Thread(target=self.mouse.run_mouse)
                                    thread_mouse.start()
                        elif command == "close" or command == "close.":
                            if len(text) > 1:
                                command2 = text[1]
                                if command2 == "mouse" or command2 == "mouse.":
                                    self.mouse.mouse_is_active = False
                        else:
                            pass

                    os.remove('speech.wav')

                except sr.WaitTimeoutError:
                    print("Listening timed out. No audio detected.")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError as e:
                    print(f"Error with the API request; {e}")

class Tutorial:
    def __init__(self, root):
        self.root = root
        self.root.title("Tutorial Window")
        self.root.geometry("800x400")

        self.label = tk.Label(self.root, text="Welcome to the Tutorial!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.label2 = tk.Label(self.root, text="Say 'Next' to proceed", font=("Arial", 16))
        self.label2.pack(pady=20)

        self.current_part = 1

        tsr = TutorialSR(self)
        threadsr = Thread(target=tsr.sr_tutorial)
        threadsr.start()

    def clear_widgets(self):
        # Destroy all widgets in the window
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_text(self, string: str):
        self.label = tk.Label(self.root, text=f"{string}", font=("Arial", 16))
        self.label.pack(pady=20)

    def next_part(self):
        self.current_part += 1

        self.clear_widgets()

        if self.current_part == 2:
            self.part_2()
        elif self.current_part == 3:
            self.part_3()
        # Add more conditions for additional parts if needed

    def part_2(self):
        self.label = tk.Label(self.root, text="This app makes use of camera for mouse movements.", font=("Arial", 16))
        self.label.pack(pady=20)

        self.label2 = tk.Label(self.root, text="First let us open camera first to enable mouse control.", font=("Arial", 16))
        self.label2.pack(pady=20)

        self.label3 = tk.Label(self.root, text="Make sure you are in a well lit room. and center you face in the camera.", font=("Arial", 16))
        self.label3.pack(pady=20)

        self.label4 = tk.Label(self.root, text="Enable it by saying 'Open mouse'.", font=("Arial", 16))
        self.label4.pack(pady=20)

    def part_3(self):
        self.label = tk.Label(self.root, text="Chuchuchuchuhuchuhcuh....", font=("Arial", 16))
        self.label.pack(pady=20)

class CameraMouse():
    mouse_is_active = False
    def __init__(self):

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

        self.sensitivity_x = 12
        self.sensitivity_y = 12

        self.adjustment_x = 205 # increase if cursor is far right from the center
        self.adjustment_y = 185 # increase if cursor is far up from the center

        screen.PAUSE=0
        screen.FAILSAFE = False

    def run_mouse(self):
        self.mouse_is_active = True

        cap = cv2.VideoCapture(0)  # 0 is index for webcams

        while self.mouse_is_active:
            ret, frame = cap.read()

            if not ret:
                print("Fucking shit what is wrong with this shit")
                break

            flipped_frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray)

            for face in faces:

                landmarks = self.predictor(gray, face)

                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                xx = landmarks.part(30).x
                yy = landmarks.part(30).y

                follow_x = xx - 205
                follow_y = yy - 185

                current_pos = screen.position()

                previous_x = xx
                previous_y = yy

                current_x = xx
                current_y = yy

                check_x = previous_x - current_x
                check_y = previous_y - current_y

                screen.moveTo(follow_x * self.sensitivity_x - current_x, follow_y * self.sensitivity_y - current_y, duration=0.1)

                cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.circle(flipped_frame, (xx, yy), 3, (255, 0, 0), -1)

            cv2.imshow('Frame', flipped_frame)

            key = cv2.waitKey(1)

            if not self.mouse_is_active:
                break
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = Tutorial(root)

    root.mainloop()
