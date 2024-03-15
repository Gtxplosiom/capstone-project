import tkinter as tk

def animate():
    max_frames = 7

    global curr_frame
    curr_frame += 1

    global curr_x, curr_y
    curr_x += 50
    curr_y += 50

    button.place(curr_x, curr_y)

    if curr_frame != max_frames:
        root.after(1000, animate)

curr_frame = 0

curr_x = 0
curr_y = 0

root = tk.Tk()
root_width = 800
root_height = 500
root.geometry(f"{root_width}x{root_height}")

button = tk.Button(root, text="Hello")
button.place(x=curr_x, y=curr_y)

root.after(3000, animate)

root.mainloop()