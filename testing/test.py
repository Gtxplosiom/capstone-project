import tkinter as tk

def after_callback():
    print("Delayed function called after button click")

def button_click():
    print("Button clicked")
    # Schedule after_callback to be called after 1000 milliseconds (1 second)
    root.after(1000, after_callback)

root = tk.Tk()

# Create a button
button = tk.Button(root, text="Click me", command=button_click)
button.pack()

root.mainloop()
