from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def CenterWindow(window):
    # Get the available screen geometry
    screen_geometry = QDesktopWidget().availableGeometry()

    # Calculate the center position for the window
    x = int((screen_geometry.width() - window.width()) / 2)
    y = int((screen_geometry.height() - window.height()) / 2)

    # Move the window to the center
    window.move(x, y)

def StartGUI():
    gui = QApplication([])
    window = QWidget()

    # Set the size of the window (optional)
    window.setGeometry(0, 0, 400, 300)
    CenterWindow(window)

    # Put elements here
    title_label = QLabel(window)
    title_label.setText("Welcome to Application!")
    title_label.setFont(QFont('Arial', 16))

    window.show()
    gui.exec_()

StartGUI()
