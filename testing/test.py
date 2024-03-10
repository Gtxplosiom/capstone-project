from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

class TutorialGUI:
    def __init__(self):

        self.app = QApplication([])

        self.window = QWidget()
        self.window.setGeometry(100, 100, 200, 300)
        
    def part_1(self):
        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Welcome to Tutorial!")
        label.setFont(QFont("Arial", 16))

        label2 = QLabel()
        label2.setText("I am here to guide you through this app")
        label2.setFont(QFont("Arial", 16))

        label3 = QLabel()
        label3.setText("Say 'Next' to proceed")
        label3.setFont(QFont("Arial", 16))

        layout.addWidget(label)
        layout.addWidget(label2)
        layout.addWidget(label3)

        self.window.setLayout(layout)

        self.window.show()
        self.app.exec_()

gui = TutorialGUI()
gui.part_1()
