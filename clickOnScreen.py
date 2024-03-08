import pyautogui
import cv2
import numpy as np
import pytesseract
import os

import win32gui, win32ui
from win32api import GetSystemMetrics

import tkinter

pytesseract.pytesseract.tesseract_cmd = (r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\tesseractOCR\tesseract.exe") # needed for Windows as OS

def HideAllRoots():
    for root in tkinter._root_window_list():
        root.withdraw()

def HighlightItems():
    dc = win32gui.GetDC(0)
    dcObj = win32ui.CreateDCFromHandle(dc)
    hwnd = win32gui.WindowFromPoint((0,0))
    monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

    while True:
        m = win32gui.GetCursorPos()

        dcObj.MoveTo((m[0], m[1]))
        dcObj.LineTo((m[0] + 30, m[1]))
        dcObj.LineTo((m[0] + 30, m[1] + 30))
        dcObj.LineTo((m[0], m[1] + 30))
        dcObj.LineTo((m[0], m[1]))

        win32gui.InvalidateRect(hwnd, monitor, True) # Refresh the entire monitor

def HighlightTk(text: str, lang='eng'):
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')
    text = text.lower()
    print(text)
    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]
        # Filter rows in DataFrame where text is equal to text
        item_instances = data[data['text'].str.lower() == text]

        num_items = len(item_instances)

        print(num_items)

        if num_items > 1:

            root = tkinter.Tk()
            root.attributes('-alpha', 0.5)
            root.attributes('-fullscreen', True)

            canvas = tkinter.Canvas(root, bg='black')
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

def Click_Image(img_loc: str, what: str):
    screenshot = pyautogui.screenshot()
    screenshot.save(r"D:\Capstone\Capstone-Application\models\screenshot.png")

    numbers = ["First", "Second", "Third", "Fourth", "FIfth", "Sixth", "Seventh", "Eighth", "Nineth", "Tenth"]
    input = numbers.index(what)

    user_img = cv2.imread(img_loc, cv2.IMREAD_GRAYSCALE)
    ref_img = cv2.imread('models/screenshot.png', cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(ref_img, user_img, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    w = user_img.shape[1]
    h = user_img.shape[0]

    threshold = 0.58

    yloc, xloc = np.where(result >= threshold)

    ## grouping of rectangles to avoid multiple matching in a single location
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        ## duplicate so that there is at least 2 rectangles on top of each other
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    ## print how many are detected
    print(len(rectangles))

    rectangles_info = []
    rectangles = sorted(rectangles, key=lambda x: x[0])  # Sort rectangles based on x-coordinates

    for i, (x, y, w, h) in enumerate(rectangles):
        cv2.rectangle(ref_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(ref_img, str(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # Print coordinates
        print(f"Rectangle {i} coordinates: x={x}, y={y}")
        rectangles_info.append((x+75, y+75))

    pyautogui.click(rectangles_info[input])
    os.remove("models/screenshot.png")

    # cv2.imshow('Reference', ref_img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

def Click(text, lang='eng'):
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')
    print(text)
    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.click(x+5, y+5)

    return(x, y)

def DoubleClick(text, lang='eng'):
    screenshot = pyautogui.screenshot()

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')

    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        pyautogui.doubleClick()
        return None

    print(x, y)

    pyautogui.doubleClick(x+5, y+5)

    return(x, y)

def Hover(text, lang='eng'):
    screenshot = pyautogui.screenshot()

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')

    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.moveTo(x+5, y+5)

    return(x, y)

def Scroll(direction):
    if direction == "up":
        pyautogui.scroll(2000)
    elif direction == "down":
        pyautogui.scroll(-2000)
    else:
        pass