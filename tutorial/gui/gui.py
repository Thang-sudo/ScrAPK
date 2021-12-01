from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QLabel, QWidget

import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        print("Clicked")

    def initUI(self):
        # Set up the window
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Scraping Project")
        # Root URL label
        self.Root_URL_Lable = QLabel(self)
        self.Root_URL_Lable.setText("Root URL")
        self.Root_URL_Lable.move(50, 25)
        # Root URL input
        self.Root_URL_Input = QLineEdit(self)
        self.Root_URL_Input.move(50,50)
        self.Root_URL_Input.resize(300, 25)
        # Title Label
        self.Title_Label = QLabel(self)
        self.Title_Label.setText("Title")
        self.Title_Label.move(50, 125)
        # Title input
        self.Title_Input = QLineEdit(self)
        self.Title_Input.move(50,150)
        self.Title_Input.resize(300, 25)
        # Package_Name Label
        self.Package_Name_Label = QLabel(self)
        self.Package_Name_Label.setText("Package Name")
        self.Package_Name_Label.move(50, 225)
        # Package_Name input
        self.Package_Name_Input = QLineEdit(self)
        self.Package_Name_Input.move(50,250)
        self.Package_Name_Input.resize(300, 25)
        # Scraping Button
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Start Scraping")
        self.b1.move(50, 300)
        self.b1.clicked.connect(self.button_clicked)


def window(): 
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()