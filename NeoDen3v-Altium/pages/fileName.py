from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGroupBox, QVBoxLayout, QGridLayout

import threading
import json


class FileNameWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent

        f = open("data/fileConfig.json", "r")
        self.fileName = json.loads(f.read())
        f.close()

        self.fields = {
            "fileName": (QLabel("File Name:"), QLineEdit(self.fileName["fileName"]))
        }

        self.buttonSave = QPushButton('SAVE')
        self.buttonSave.setStyleSheet('QPushButton {background-color:#0000FF;font:bold}')
        self.buttonSave.clicked.connect(self.clickedSave)

        self.buttonBack = QPushButton('BACK')
        self.buttonBack.setStyleSheet('QPushButton {background-color:#999999;font:bold}')
        self.buttonBack.clicked.connect(self.clickedBack)

        self.loadWindow()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox2 = QGroupBox()
        layout = QGridLayout()
        layout2 = QGridLayout()

        c = 0
        for field in self.fields.values():
            layout.addWidget(field[0], c, 0)
            layout.addWidget(field[1], c, 1)
            c+=1

        layout2.addWidget(self.buttonSave, 0, 0)
        layout2.addWidget(self.buttonBack, 0, 1)

        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBox2.setLayout(layout2)

    def loadWindow(self):
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle("Set File Name")

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox2)
        self.setLayout(windowLayout)
        self.show()

    def clickedSave(self):
        valuesToSave = {}
        for field in self.fields:
            valuesToSave[field] = self.fields[field][1].text()
        self.buttonSave.setStyleSheet('QPushButton {background-color:#FF0000;font:bold}')
        threading.Thread(target=self.eventSave, args=(valuesToSave,)).start()
        self.mainWindow.show()
        self.close()

    def eventSave(self, valuesToSave):
        f = open("data/fileConfig.json", "w")
        f.write(json.dumps(valuesToSave, indent=4))
        f.close()
        self.buttonSave.setStyleSheet('QPushButton {background-color:#0FB328;font:bold}')

    def clickedBack(self):
        self.mainWindow.show()
        self.close()
