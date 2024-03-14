import tkinter as tk
from threading import Thread
import os
import time
import whisper
import speech_recognition as sr
import keyboard

import cv2
import dlib
import pyautogui
import numpy as np
import pytesseract

class TutorialSR:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = script_dir.replace('\\', '/')
    tiny_model_path = os.path.expanduser(f'{script_dir}/models/tiny.en.pt')

    is_listening = True
    def __init__(self, tutorial):
        self.tutorial = tutorial
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.tiny_model = whisper.load_model(self.tiny_model_path)

        self.in_tutorial = True

        self.mouse = CameraMouse()

        self.symbols = ['!', ',', '.', '?']

    def audio_to_wav(self, audio):
        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    def transcribe_to_text(self, model):
        try:
            result = model.transcribe('speech.wav')

            text = result['text']
            text = text.lower()
            text = text.split(' ')
            text.remove(text[0])

            return text
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            os._exit(0)
    
    @staticmethod
    def capitalize_word(word: str):
        new_text = []

        index = 0

        for letter in word:
            new_text.append(word[index].capitalize())
            index += 1

        new_text = ''.join(new_text)

        return new_text
    
    @staticmethod
    def exit_program(e):
        if e.name == 'esc':
            print("Exiting the program...")
            os._exit(0)

    keyboard.on_press(exit_program)
    
    def check_mic(self):
        while True:
            time.sleep(0.1)

            if self.is_listening:
                self.tutorial.listen_label.config(text="Listening...")
            else:
                self.tutorial.listen_label.config(text="Processing audio")
    
    # Page segmentation modes: for OCR
    # 0    Orientation and script detection (OSD) only.
    # 1    Automatic page segmentation with OSD.
    # 2    Automatic page segmentation, but no OSD, or OCR.
    # 3    Fully automatic page segmentation, but no OSD. (Default)
    # 4    Assume a single column of text of variable sizes.
    # 5    Assume a single uniform block of vertically aligned text.
    # 6    Assume a single uniform block of text.
    # 7    Treat the image as a single text line.
    # 8    Treat the image as a single word.
    # 9    Treat the image as a single word in a circle.
    # 10    Treat the image as a single character.
    # 11    Sparse text. Find as much text as possible in no particular order.
    # 12    Sparse text with OSD.
    # 13    Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
    
    @staticmethod
    def HighlightTk(text: str, lang='eng'):
        screenshot = pyautogui.screenshot()

        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        psm_num = 6 # adjust page segmentation mode for better extraction of text depending on your image
        custom_config = f'--oem 3 --psm {psm_num}'
        data = pytesseract.image_to_data(img, config=custom_config, lang=lang, output_type='data.frame')

        min_conf = 85

        try:
            data = data[(data['text'] == text) & (data['conf'] >= min_conf)]
            x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]
            # Filter rows in DataFrame where text is equal to text
            item_instances = data[data['text'] == text]

            num_items = len(item_instances)

            print(item_instances)
            print(num_items)

            if num_items > 1:
                root = tk.Tk()
                root.attributes('-alpha', 0.5)
                root.attributes('-fullscreen', True)

                canvas = tk.Canvas(root, bg='black')
                canvas.pack(fill='both', expand=True)

                print(num_items)

                # Loop through each instance of the input text and draw a rectangle with a label
                for idx, (index, row) in enumerate(item_instances.iterrows(), 1):
                    x1, y1 = row['left'], row['top']
                    width, height = row['width'], row['height']
                    x2, y2 = x1 + width, y1 + height

                    canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

                    # Label the found item with a number above the rectangle
                    label_x = (x1 + x2) / 2
                    label_y = y1 - 10
                    canvas.create_text(label_x, label_y, text=str(idx), fill='white')
                
                root.after(5000, root.destroy)

                root.mainloop()
            else:
                pyautogui.click(x, y)

        except IndexError:
            print("Text was not found")
            return None
        
        return(x, y)

    def sr_tutorial(self):
        while self.in_tutorial:
            with self.mic as source:

                print("Listening. In tutorial...")
                self.is_listening = True

                self.r.adjust_for_ambient_noise(source)
                try:
                    audio = self.r.listen(source)

                    self.is_listening = False

                    self.audio_to_wav(audio)

                    text = self.transcribe_to_text(self.tiny_model)

                    if len(text) > 0:
                        command = text[0]
                        for x in self.symbols:
                            command = command.replace(x, '')
                        print(command)

                        if command == "next":
                            self.tutorial.next_part()
                        if command == "forward":
                            self.tutorial.part_8()
                        elif command == "open":
                            if len(text) > 1:
                                command2 = text[1]
                                for x in self.symbols:
                                    command2 = command2.replace(x, '')
                                if command2 == "mouse":
                                    self.tutorial.add_text("Opening mouse. Wait for a sec...")
                                    self.tutorial.add_text("Say 'Next' to proceed.")
                                    thread_mouse = Thread(target=self.mouse.run_mouse)
                                    thread_mouse.start()
                        elif command == "close":
                            if len(text) > 1:
                                command2 = text[1]
                                for x in self.symbols:
                                    command2 = command2.replace(x, '')
                                if command2 == "mouse":
                                    self.mouse.mouse_is_active = False
                        elif command == "click":
                            if len(text) > 1:
                                command2 = text[1]

                                for x in self.symbols:
                                    command2 = command2.replace(x, '')

                                command2 = self.capitalize_word(command2)

                                print(command2)

                                self.HighlightTk(command2)
                            else:
                                pyautogui.click()
                        else:
                            pass
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
        self.center_window(self.root, 800, 400)

        self.listen_window = tk.Toplevel()
        self.listen_window.title("Check if listening or processing audio")
        self.listen_window.geometry("400x200+1500+700")

        self.label = tk.Label(self.root, text="Welcome to the Tutorial!", font=("Arial", 16))
        self.label.pack(pady=20)

        self.label2 = tk.Label(self.root, text="Say 'Next' to proceed", font=("Arial", 16))
        self.label2.pack(pady=20)

        self.label3 = tk.Label(self.root, text="", font=("Arial", 16))
        self.label4 = tk.Label(self.root, text="", font=("Arial", 16))

        self.listen_label = tk.Label(self.listen_window, text="not checking mic...", font=("Arial", 16))
        self.listen_label.pack(pady=20)

        self.other_label = tk.Label(self.root)

        self.button1 = tk.Button(self.root)
        self.button2 = tk.Button(self.root)
        

        self.current_part = 1

        pytesseract.pytesseract.tesseract_cmd = (r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\tesseractOCR\tesseract.exe") # needed for Windows as OS

        tsr = TutorialSR(self)
        threadsr = Thread(target=tsr.sr_tutorial)
        threadsr.start()

        thread_check_mic = Thread(target=tsr.check_mic)
        thread_check_mic.start()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_coordinate = (screen_width - width) // 2
        y_coordinate = (screen_height - height) // 2

        window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

    def clear_widgets(self, num: int):
        time.sleep(num)
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def add_text(self, string: str):
        self.other_label.configure(text=f"{string}", font=("Arial", 16))
        self.other_label.pack(pady=20)

    def delayed_text(self, num: int, text: str):
        time.sleep(num)
        self.add_text(f"{text}")

    def change_color(self, what: object, color: str):
        what.configure(bg=color)

    def change_color_next(self, what: object, color: str):
        what.configure(bg=color)

        current_color = what.cget("bg")

        if current_color == color:
            self.next_part()
        else:
            pass

    def next_part(self):
        self.current_part += 1

        if self.current_part == 2:
            self.part_2()
        elif self.current_part == 3:
            self.part_3()
        elif self.current_part == 4:
            self.part_4()
        elif self.current_part == 5:
            self.part_5()
        elif self.current_part == 6:
            self.part_6()
        elif self.current_part == 7:
            self.part_7()
        elif self.current_part == 8:
            self.part_8()
        elif self.current_part == 9:
            self.part_9()
        elif self.current_part == 10:
            self.part_10()
        else:
            print("Part doesn't exist.")

    def part_2(self):
        self.label.configure(text="This app makes use of camera for mouse movements.", font=("Arial", 16))

        self.label2.configure(text="First let us open camera first to enable mouse control.", font=("Arial", 16))

        self.label3.configure(text="Make sure you are in a well lit room. and center you face in the camera.", font=("Arial", 16))
        self.label3.pack(pady=20)

        self.label4.configure(text="Enable it by saying 'Open mouse'.", font=("Arial", 16))
        self.label4.pack(pady=20)

    def part_3(self):
        self.label2.pack_forget()
        self.label3.pack_forget()
        self.label4.pack_forget()

        self.label.configure(text="Try moving your head around", font=("Arial", 16))

        thread_dt = Thread(target=self.delayed_text, args=(10, "Say 'Next' to proceed."))
        thread_dt.start()

    def part_4(self):
        self.other_label.pack_forget()

        self.label.configure(text="You probably noticed that you can command the", font=("Arial", 16))

        self.label2.configure(text="application by telling it what to do", font=("Arial", 16))
        self.label2.pack(pady=20)

        thread_dt = Thread(target=self.delayed_text, args=(5, "There are tons of commands that you can say to the application.\nLet's try some right now!\n \n Say 'Next' to proceed."))
        thread_dt.start()

    def part_5(self):
        self.label2.pack_forget()
        self.other_label.pack_forget()

        self.label.configure(text="Let us execute the basic mouse functions first.", font=("Arial", 16))
        
        time.sleep(3)

        self.label.configure(text="Let us try to press something on the screen", font=("Arial", 16))

        self.delayed_text(3, "Guide the cursor to the button and say \n'Click' to change the color of the window")

        self.button1.configure(text="Change color", command=lambda: self.change_color_next(self.root, "cyan"), width=50, height=25)
        self.button1.pack(pady=20)

    def part_6(self):
        self.other_label.pack_forget()

        self.label.configure(text="Good job! You can use the 'Click' command when \n you want to utilize the left-click function of the mouse. \n You can use this to click menus or applications in the taskbar. \n \n Click 'Next' to Proceed", font=("Arial", 16))

        self.button1.configure(text="Next", command=self.next_part, width=30, height=15)

    def part_7(self):
        self.button1.pack_forget()

        self.label.configure(text="You can close the camera controlled mouse by saying 'Close mouse' command. \n \n Try it right now.", font=("Arial", 16))

        self.delayed_text(5, "Say 'Next' to continue.")

    def part_8(self):
        self.other_label.pack_forget()

        self.label.configure(text="Alternatively, when the mouse is disabled, you can directly click \n something on the screen by saying 'Click' first then \n saying the word associated with what you wanted to click. \n Try clicking the two buttons on the screen.", font=("Arial", 16))

        self.button1.configure(text="GREEN", font=("Arial", 20), bg="white", command=lambda: self.change_color(self.root, "green"), width=20, height=10)
        self.button1.pack(side="left", padx=10)

        self.button2.configure(text="BLUE", font=("Arial", 20), bg="white", command=lambda: self.change_color(self.root, "blue"), width=20, height=10)
        self.button2.pack(side="left")

        thread_dt = Thread(target=self.delayed_text, args=(15, "Say 'Next' to proceed."))
        thread_dt.start()

    def part_9(self):
        self.other_label.pack_forget()
        self.button1.pack_forget()
        self.button2.pack_forget()

        self.label.configure(text="Moving on, let us try the 'Double-click' command.")

        time.sleep(3)

        self.label.configure(text="This command is commonly used in opening desktop icons or items\n in the windows file manager.")

        time.sleep(5)

        

    def part_10(self):
        pass
        
class CameraMouse():
    mouse_is_active = False
    def __init__(self):

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

        self.sensitivity_x = 12
        self.sensitivity_y = 12

        self.adjustment_x = 205 # increase if cursor is far right from the center
        self.adjustment_y = 185 # increase if cursor is far up from the center

        pyautogui.PAUSE=0
        pyautogui.FAILSAFE = False

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

                current_pos = pyautogui.position()

                previous_x = xx
                previous_y = yy

                current_x = xx
                current_y = yy

                check_x = previous_x - current_x
                check_y = previous_y - current_y

                pyautogui.moveTo(follow_x * self.sensitivity_x - current_x, follow_y * self.sensitivity_y - current_y, duration=0.1)

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