import pyautogui
import time
import clickOnScreen

class FocusThings:
    def __init__(self):
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

    if command == "Login":
        if len(string) > 1:
            command = string[1].capitalize()
            img_loc = "models/shesh.png"
            print("clicking image...")
            clickOnScreen.Click_Image(img_loc, command)
        else:
            pass
    elif command == "Log":
        if len(string) > 2:
            if string[1] == "in":
                command2 = string[2].capitalize()
                img_loc = "models/shesh.png"
                print("clicking image...")
                clickOnScreen.Click_Image(img_loc, command2)
        else:
            pass
    elif command == "Search":
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
        if len(string) > 1:
            command2 = string[1]
            list = ["once", "twice", "thrice"]
            command2 = list.index(command2)
            for x in range(command2):
                time.sleep(0.1)
                pyautogui.hotkey('down')
        else:
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

def Guide(string: str):
    from tutorial import Tutorial

    string = string[1:].split(" ")
    command = string[0].capitalize()
    text = ' '.join(string[1:])

    if command == "Next":
        Tutorial.game_state += 1