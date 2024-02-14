import tkinter
import cv2
import pytesseract
import pyautogui
import numpy as np
import time

screenshot = pyautogui.screenshot()
img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

data = pytesseract.image_to_data(img, lang='eng', output_type='data.frame')
text = "File"

try:
    # Filter rows in DataFrame where text is equal to "File"
    file_instances = data[data['text'] == text]

    # Create a Tkinter window
    root = tkinter.Tk()
    root.attributes('-alpha', 0.5)
    root.attributes('-fullscreen', True)

    # Create a Canvas widget
    canvas = tkinter.Canvas(root, bg='black')
    canvas.pack(fill='both', expand=True)

    print(len(file_instances))

    # Loop through each instance of "File" and draw a rectangle with a label
    for idx, (index, row) in enumerate(file_instances.iterrows(), 1):
        x1, y1 = row['left'], row['top']
        width, height = row['width'], row['height']
        x2, y2 = x1 + width, y1 + height

        # Draw a blue rectangle around each instance of "File"
        canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

        # Label the found item with a number above the rectangle
        label_x = (x1 + x2) / 2
        label_y = y1 - 10  # Adjust the y position to be above the rectangle
        canvas.create_text(label_x, label_y, text=str(idx), fill='white')

    root.after(5000, root.destroy)

    root.mainloop()

except IndexError:
    print("Text was not found")
