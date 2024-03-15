import tkinter as tk
import os

class Window:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1000x580')

        self.fm_icon = tk.PhotoImage(file='media/icons/fmicon.png')
        self.close_icon = tk.PhotoImage(file='media/icons/close.png')
        self.folder_icon = tk.PhotoImage(file='media/icons/folder.png')
        self.image_icon = tk.PhotoImage(file='media/icons/image.png')
        self.mp4_icon = tk.PhotoImage(file='media/icons/mp4.png')
        self.windows_app_icon = tk.PhotoImage(file='media/icons/windows_app.png')

        self.click_count = 0

        self.file_manager()

    def file_manager(self):
        fm_root = tk.Toplevel()
        fm_root.wm_attributes('-topmost', True)
        fm_root.overrideredirect(True)
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

    def close_window(self, window):
        window.destroy()

    def reset_clicks(self):
        self.click_count = 0

    def double_click(self, button):
        self.click_count += 1
        self.root.after(200, self.reset_clicks)
        if self.click_count == 2:
            print(f"clicked by {button}")
            self.reset_clicks()

if __name__ == '__main__':
    root = tk.Tk()
    window = Window(root)

    root.mainloop()
