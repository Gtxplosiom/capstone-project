import pygetwindow as gw
import time

def get_active_window_title():
    return gw.getActiveWindow().title if gw.getActiveWindow() else None

previous_active_window = None

while True:
    current_active_window = get_active_window_title()

    if current_active_window != previous_active_window:
        print("Active Window:", current_active_window)
        previous_active_window = current_active_window

    time.sleep(1)
