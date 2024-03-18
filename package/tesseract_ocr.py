import os

import tkinter as tk
import numpy as np
import pyautogui
import pytesseract
import cv2

class TesseractOCR:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = script_dir.replace('\\', '/')
    tesseract_path = os.path.expanduser(f'{curr_dir}/assets/tesseractOCR/tesseract.exe')
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = (self.tesseract_path)

    def one_to_many(text: str, lang='eng'):
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
                root = tk.Toplevel()
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
            else:
                pyautogui.click(x, y)

        except IndexError:
            print("Text was not found")
            return None
        
        return(x, y)
