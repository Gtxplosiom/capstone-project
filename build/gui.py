
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Capstone\Capstone-Application\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.wm_attributes('-toolwindow', 'true')

window.geometry("1000x580")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 580,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    580.0,
    fill="#FFFFFF",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=630.0,
    y=210.0,
    width=89.0,
    height=89.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=451.0,
    y=210.0,
    width=89.0,
    height=89.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=263.0,
    y=205.0,
    width=98.0,
    height=98.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=75.0,
    y=210.0,
    width=98.0,
    height=89.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=956.0,
    y=14.0,
    width=28.284271240234375,
    height=28.2843017578125
)

canvas.create_rectangle(
    5.0,
    6.0,
    244.0,
    106.0,
    fill="#E8E8E8",
    outline="")

canvas.create_rectangle(
    0.0,
    56.0,
    1000.0,
    156.0,
    fill="#E8E8E8",
    outline="")

canvas.create_text(
    52.0,
    24.0,
    anchor="nw",
    text="sample folder",
    fill="#000000",
    font=("InriaSans Bold", 12 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    34.0,
    32.0,
    image=image_image_1
)

canvas.create_text(
    108.0,
    299.0,
    anchor="nw",
    text="Files",
    fill="#000000",
    font=("InriaSans Bold", 12 * -1)
)

canvas.create_text(
    640.0,
    299.0,
    anchor="nw",
    text="Application",
    fill="#000000",
    font=("InriaSans Bold", 12 * -1)
)

canvas.create_text(
    482.0,
    303.0,
    anchor="nw",
    text="Video",
    fill="#000000",
    font=("InriaSans Bold", 12 * -1)
)

canvas.create_text(
    303.0,
    303.0,
    anchor="nw",
    text="Photo",
    fill="#000000",
    font=("InriaSans Bold", 12 * -1)
)

window.resizable(False, False)
window.mainloop()
