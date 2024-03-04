import pyautogui
import time

def Tutorial(command: str):
    ## commands block
    string = string[1:].split(" ")
    command = string[0].capitalize()
    text = ' '.join(string[1:])

    if command == "Next":
        pass


def MouseScroll():
    screen_width, screen_height = pyautogui.size()

    x_coordinate = screen_width - 1  # Rightmost side
    y_coordinate = screen_height // 2  # Center vertically

    pyautogui.moveTo(x_coordinate, y_coordinate)

def Notepad():
    pass
                
def Word():
    pass

def Chrome(string: str):
    ## commands block
    string = string[1:].split(" ")
    command = string[0].capitalize()
    text = ' '.join(string[1:])

    if command == "Search":
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.1)
        pyautogui.hotkey('backspace')
    elif command == "Write" or command == "Right":
        print("Writing something...")
        pyautogui.typewrite(str(text))
    elif command == "Enter":
        pyautogui.hotkey('enter')
    elif command == "Up":
        pyautogui.hotkey('up')
    elif command == "Down":
        pyautogui.hotkey('down')
    elif "New tab" in command:
        pyautogui.hotkey('ctrl', 't')
    elif command == "Close":
        pyautogui.hotkey('ctrl', 'w')
    elif command == "Maximize" or command == "Maximise":
        pyautogui.hotkey('alt', 'space')
        time.sleep(0.1)
        pyautogui.hotkey('x')
    elif command == "Click":
        pyautogui.click()
    elif "close browser" in command:
        pass
    else:
        pass