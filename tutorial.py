from threading import Thread
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

import numpy as np
import tkinter as tk
import speech_recognition as sr
import whisper
import keyboard
import cv2
import pyautogui
import pytesseract

from package import CameraMouse
from package import SeleniumBrowser
from package import TesseractOCR

class TutorialSR:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = script_dir.replace('\\', '/')
    model_path = '/package/assets/models/sr_stuff/whisper_stuff/models'
    tiny_model_path = os.path.expanduser(f'{curr_dir}{model_path}/english_only/tiny.en.pt')

    is_listening = True

    def __init__(self, tutorial):
        self.tutorial = tutorial
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()

        self.tiny_model = whisper.load_model(self.tiny_model_path)

        self.in_tutorial = True

        self.cm = CameraMouse()
        self.browser = SeleniumBrowser()
        self.ocr = TesseractOCR()

        self.symbols = ['!', ',', '.', '?']

    def audio_to_wav(self, audio):
        with open('speech.wav', 'wb') as f:
            f.write(audio.get_wav_data())

    def transcribe_to_text(self, model):
        try:
            result = model.transcribe('speech.wav', fp16=False)

            text = result['text']
            text = text.lower()
            text = text.split(' ')
            text.remove(text[0])

            return text
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            os._exit(0)
    
    @staticmethod
    def capitalize_all_letters(word: str):
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

    def sr_tutorial(self):
        while self.in_tutorial:
            with self.mic as source:
                if self.browser.browser_is_active:
                    print("Listening. In browser...")

                    self.is_listening = True

                    self.r.adjust_for_ambient_noise(source)

                    try:
                        audio = self.r.listen(source)

                        self.is_listening = False

                        self.audio_to_wav(audio)

                        text = self.transcribe_to_text(self.tiny_model)

                        text = ' '.join(text)

                        self.browser.execute_in_browser(text)

                        os.remove('speech.wav')

                    except sr.WaitTimeoutError:
                        print("Listening timed out. No audio detected.")
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Error with the API request; {e}")
                else:
                    print("Listening. In tutorial...")
                    self.is_listening = True

                    self.r.adjust_for_ambient_noise(source)

                    try:
                        audio = self.r.listen(source)

                        self.is_listening = False

                        self.audio_to_wav(audio)

                        text = self.transcribe_to_text(self.tiny_model)

                        print(text)

                        if len(text) > 0:
                            command = text[0]
                            for x in self.symbols:
                                command = command.replace(x, '')

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
                                        thread_mouse = Thread(target=self.cm.run_mouse)
                                        thread_mouse.start()
                                    elif command2 == "browser":
                                        thread_browser = Thread(target=self.browser.open_browser)
                                        thread_browser.start()
                            elif command == "close":
                                if len(text) > 1:
                                    command2 = text[1]
                                    for x in self.symbols:
                                        command2 = command2.replace(x, '')
                                    if command2 == "mouse":
                                        self.cm.mouse_is_active = False
                            elif command == "click":
                                if len(text) > 1:
                                    command2 = text[1]

                                    for x in self.symbols:
                                        command2 = command2.replace(x, '')

                                    command2 = self.capitalize_all_letters(command2)

                                    self.ocr.one_to_many(command2)
                                else:
                                    pyautogui.click()
                            elif command == "double":
                                if len(text) > 1:
                                    command2 = text[1]

                                    for x in self.symbols:
                                        command2 = command2.replace(x, '')

                                    if command2 == "click":
                                        pyautogui.doubleClick()
                                        if len(text) > 2:
                                            command3 = text[2]
                                            self.HighlightTk(command2)
                                        else:
                                            pass
                                    else:
                                        pass
                                pass
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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tesseract_path = os.path.expanduser(f'{script_dir}\\package\\assets\\tesseractOCR\\tesseract.exe')

    colors = {'Rich black': '#031926', 'Teal': '#468189', 'Cambridge blue': '#77ACA2', 'Ash gray': '#9DBEBB', 'Parchment': '#F4E9CD', }
    
    def __init__(self, root):
        pytesseract.pytesseract.tesseract_cmd = (self.tesseract_path) # needed for Windows as OS

        self.root = root
        self.root.title("Tutorial Window")
        self.root.configure(bg=self.colors['Teal'])
        self.center_window(self.root, 800, 400)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.listen_window = tk.Toplevel()
        self.listen_window.overrideredirect(True)
        self.listen_window.wm_attributes('-topmost', True)
        self.listen_window.title("Check if listening or processing audio")
        self.listen_window.configure(bg=self.colors['Teal'])

        self.lw_width = 400
        self.lw_height = 200
        self.x_position = self.screen_width - self.lw_width
        self.y_position = 700

        self.listen_window.geometry(f"{self.lw_width}x{self.lw_height}+{self.x_position}+{self.y_position}")

        self.label = tk.Label(self.root, text="Welcome to the Tutorial!", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])
        self.label.pack(pady=20)

        self.label2 = tk.Label(self.root, text="Say 'Next' to proceed", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])
        self.label2.pack(pady=20)

        self.label3 = tk.Label(self.root, text="", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])
        self.label4 = tk.Label(self.root, text="", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])

        self.listen_label = tk.Label(self.listen_window, text="not checking mic...", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])
        self.listen_label.pack(pady=20)

        self.other_label = tk.Label(self.root)

        self.button1 = tk.Button(self.root)
        self.button2 = tk.Button(self.root)

        # file manager attributes
        self.fm_icon = tk.PhotoImage(file="package/assets/media/icons/fmicon.png")
        self.close_icon = tk.PhotoImage(file="package/assets/media/icons/close.png")
        self.folder_icon = tk.PhotoImage(file="package/assets/media/icons/folder.png")
        self.image_icon = tk.PhotoImage(file="package/assets/media/icons/image.png")
        self.mp4_icon = tk.PhotoImage(file="package/assets/media/icons/mp4.png")
        self.windows_app_icon = tk.PhotoImage(file="package/assets/media/icons/windows_app.png")

        self.click_count = 0

        self.current_part = 1

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
        self.other_label.configure(text=f"{string}", font=("Arial", 16), fg=self.colors['Parchment'], bg=self.colors['Teal'])
        self.other_label.pack(pady=20)

    def delayed_text(self, num: int, text: str):
        time.sleep(num)
        self.add_text(f"{text}")

    def label_color(self, fg_color, bg_color):
        self.label.configure(fg=fg_color, bg=bg_color)
        self.label2.configure(fg=fg_color, bg=bg_color)
        self.label3.configure(fg=fg_color, bg=bg_color)
        self.label4.configure(fg=fg_color, bg=bg_color)

        self.other_label.configure(fg=fg_color, bg=bg_color)

    def change_color(self, what: object, color: str):
        what.configure(bg=color)

        self.label_color(self.colors['Parchment'], color)

    def change_color_next(self, what: object, color: str):
        what.configure(bg=color)

        self.label_color(self.colors['Rich black'], color)

        current_color = what.cget("bg")

        if current_color == color:
            self.next_part()
        else:
            pass

    def close_window(self, window):
        window.destroy()

    def reset_clicks(self):
        self.click_count = 0

    def double_click(self, button):
        self.click_count += 1
        self.root.after(200, self.reset_clicks)
        if self.click_count == 2:
            print(f'clicked by {button}')
            if button == 'folder_button':
                self.open_folder()
            elif button == 'photo_button':
                self.open_photo()
            elif button == 'video_button':
                self.open_video()
            elif button == 'app_button':
                self.open_app()

            self.reset_clicks()

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
            self.current_part -= 1
            print("Part does not exist.")

    def file_manager(self):
        fm_root = tk.Toplevel()
        fm_root.wm_attributes('-topmost', True)
        fm_root.overrideredirect(True)
        fm_root.geometry('1000x580+50+200')
        fm_root.configure(bg='#FFFFFF')

        top_part = tk.Frame(fm_root, bg='#FFFFFF', width=1000, height=156)
        top_part.pack(side='top')

        bottom_part = tk.Frame(fm_root, bg='#FFFFFF', width=1000, height=424)
        bottom_part.pack(side='bottom')

        header_1 = tk.Frame(top_part, bg='#E9E9E9', width=239, height=100)
        header_1.place(x=5, y=6)
        title = tk.Label(header_1, text="sample folder", bg='#E9E9E9')
        title.place(x=52, y=15)

        fm_logo = tk.Label(header_1, image=self.fm_icon, bg='#E9E9E9')
        fm_logo.place(x=10, y=10)

        header_2 = tk.Frame(top_part, bg='#E9E9E9', width=1000, height=580)
        header_2.place(x=0, y=56)

        close_button = tk.Button(top_part, image=self.close_icon, bg='#FFFFFF', bd=0, command=lambda: self.close_window(fm_root))
        close_button.place(x=956, y=14)

        folder_button = tk.Button(bottom_part, image=self.folder_icon, bg='#FFFFFF', bd=0, command=lambda: self.double_click("folder_button"))
        folder_button.place(x=75, y=50)
        folder_text = tk.Label(bottom_part, text="File", font=('arial', 12), bg='#FFFFFF')
        folder_text.place(x=108, y=145)

        photo_button = tk.Button(bottom_part, image=self.image_icon, bg='#FFFFFF', bd=0, command=lambda: self.double_click("photo_button"))
        photo_button.place(x=263, y=50)
        photo_text = tk.Label(bottom_part, text="Photo", font=('arial', 12), bg='#FFFFFF')
        photo_text.place(x=290, y=145)

        video_button = tk.Button(bottom_part, image=self.mp4_icon, bg='#FFFFFF', bd=0, command=lambda: self.double_click("video_button"))
        video_button.place(x=451, y=50)
        video_text = tk.Label(bottom_part, text="Video", font=('arial', 12), bg='#FFFFFF')
        video_text.place(x=473, y=145)

        app_button = tk.Button(bottom_part, image=self.windows_app_icon, bg='#FFFFFF', bd=0, command=lambda: self.double_click("app_button"))
        app_button.place(x=630, y=50)
        app_text = tk.Label(bottom_part, text="Application", font=('arial', 12), bg='#FFFFFF')
        app_text.place(x=635, y=145)

        def show_next():
            label = tk.Label(bottom_part, text='Say "Next" if you are done.', font=('arial', 16), bg='#FFFFFF')
            label.place(x=350, y=250)

        self.root.after(30000, show_next)

    def open_folder(self):
        folder = tk.Toplevel()
        folder.wm_attributes('-topmost', True)
        folder.configure(bg='#FFFFFF')

        top_part = tk.Frame(folder, bg='#FFFFFF', width=1000, height=156)
        top_part.pack(side='top')

        bottom_part = tk.Frame(folder, bg='#FFFFFF', width=1000, height=424)
        bottom_part.pack(side='bottom')

        header_1 = tk.Frame(top_part, bg='#E9E9E9', width=239, height=100)
        header_1.place(x=5, y=6)
        title = tk.Label(header_1, text="File", bg='#E9E9E9')
        title.place(x=52, y=15)

        fm_logo = tk.Label(header_1, image=self.fm_icon, bg='#E9E9E9')
        fm_logo.place(x=10, y=10)

        header_2 = tk.Frame(top_part, bg='#E9E9E9', width=1000, height=580)
        header_2.place(x=0, y=56)

        close_button = tk.Button(top_part, image=self.close_icon, bg='#FFFFFF', bd=0, command=lambda: self.close_window(folder))
        close_button.place(x=956, y=14)

    def open_photo(self):
        img = Image.open('media/Facebook.png')
        img.show()

    def open_video(self):
        vid = Image.open('media/sample_vid.gif')
        vid.show()

    def open_app(self):
        app = tk.Toplevel()
        app.wm_attributes('-topmost', True)
        app.configure(bg='#FFFFFF')
        app.geometry('800x500')

        app_label = tk.Label(app, text="This app is currently running...")
        app_label.pack()
    
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

        thread_dt = Thread(target=self.delayed_text, args=(5, "Say 'Next' to continue."))
        thread_dt.start()

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

        self.root.configure(bg=self.colors['Teal'])
        self.label_color(self.colors['Parchment'], self.colors['Teal'])

        self.label.configure(text="Moving on, let us try the 'Double-click' command.")

        time.sleep(3)

        self.label.configure(text="This command is commonly used in opening desktop icons or items\n in the windows file manager.")

        time.sleep(5)

        self.next_part()

    def part_10(self):
        self.label.pack_forget()
        self.root.geometry('800x400+1100+200')

        self.label.configure(text="Try to open the folder, photo, video, and the app \n with the 'Double click' command. \n\n Once you are done say 'Next' to proceed")

        self.file_manager()

    def part_11(self):
        self.label.pack_forget()
        self.listen_window.destroy()
        self.center_window(self.root, 800, 400)

        self.label.configure(text="Now that we've covered all the basics, \n let us now use some applications")

        time.sleep(2)

        self.label.configure(text="You can say 'Open' command following the application \n that you want to open")

        time.sleep(3)

        self.label.pack_forget()

        thread_dt = Thread(target=self.delayed_text, args=(2, "Let us browser the internet!"))
        thread_dt.start()

        thread_dt = Thread(target=self.delayed_text, args=(2, "Say 'Open browser' to open the browser"))
        thread_dt.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_attributes('-topmost', 'true')
    app = Tutorial(root)

    root.mainloop()