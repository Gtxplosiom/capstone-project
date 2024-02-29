from customtkinter import *

def open_new_window(previous_window):
    # Destroy the current window
    previous_window.destroy()

    # Create a new window
    new_window = CTk()
    new_window.geometry("400x300")

    new_label = CTkLabel(master=new_window, text="New Window!")
    new_label.pack(pady=20)

    new_button = CTkButton(master=new_window, text="Close", command=new_window.destroy)
    new_button.pack(pady=20)

    new_window.mainloop()

def MainWindow():
    window = CTk()
    window.geometry("500x400")

    label = CTkLabel(master=window, text="Welcome!")
    label.place(relx=0.5, rely=0.2, anchor="center")

    btn = CTkButton(master=window, text="Next", command=lambda: open_new_window(window))
    btn.place(relx=0.5, rely=0.5, anchor="center")

    window.mainloop()

MainWindow()
