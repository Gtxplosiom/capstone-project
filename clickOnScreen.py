import pyautogui
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (r"C:\Users\admin\Desktop\TRYZLER\Capstone-Application\tesseractOCR\tesseract.exe") # needed for Windows as OS

def clickPic(icon):
    pyautogui.click(f'media\{icon}.png')

def click(text, lang='eng'):
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

def doubleClick(text, lang='eng'):
    screenshot = pyautogui.screenshot()

    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    data = pytesseract.image_to_data(img, lang=lang, output_type='data.frame')

    try:
        x, y = data[data['text'] == text]['left'].iloc[0], data[data['text'] == text]['top'].iloc[0]

    except IndexError:
        print("Text was not found")
        return None

    print(x, y)

    pyautogui.doubleClick(x+5, y+5)

    return(x, y)

def hover(text, lang='eng'):
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