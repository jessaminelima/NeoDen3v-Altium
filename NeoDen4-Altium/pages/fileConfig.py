from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QLineEdit, QLabel, QGroupBox, QVBoxLayout, QGridLayout

import json
import threading


class FileConfigWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent

        f = open("data/fileConfig.json", "r")
        self.fileName = json.loads(f.read())
        f.close()

        self.file = self.fileName["fileName"]

        self.fields = {
            "xSize": (QLabel("PCB X Size:"), QLineEdit("0"))

        }
        self.buttonCont = QPushButton('Continue')
        self.buttonCont.setStyleSheet('QPushButton {background-color:#0000FF;font:bold}')
        self.buttonCont.clicked.connect(self.clickedCont)

        self.buttonBack = QPushButton('Back')
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
            c += 1

        layout2.addWidget(self.buttonCont, 0, 0)
        layout2.addWidget(self.buttonBack, 0, 1)

        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBox2.setLayout(layout2)

    def loadWindow(self):
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle("Set PCB Size")

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBox2)
        self.setLayout(windowLayout)
        self.show()

    def clickedCont(self):
        valuesToSave = self.fileName
        for field in self.fields:
            valuesToSave[field] = float(self.fields[field][1].text())
        self.buttonCont.setStyleSheet('QPushButton {background-color:#000080;font:bold}')
        threading.Thread(target=self.eventSave, args=(valuesToSave,)).start()
        self.Parameters("data/" + valuesToSave["fileName"], valuesToSave["xSize"])

    def eventSave(self, valuesToSave):
        f = open("data/fileConfig.json", "w")
        f.write(json.dumps(valuesToSave, indent=4))
        f.close()
        self.buttonCont.setStyleSheet('QPushButton {background-color:#0000FF;font:bold}')

    def clickedBack(self):
        self.mainWindow.show()
        self.close()

    def Parameters(self, file_name, x_size):
        # Opening Altium .cvs file
        altiumOutputFile = open(file_name, "r", encoding="latin1")
        pickPlace = altiumOutputFile.read()
        altiumOutputFile.close()

        # Removing Altium Header's and BlankLine
        pickPlace = pickPlace.split("\n")[13:-1]
        buffer = []

        # Removing "
        for col in range(len(pickPlace)):
            pickPlace[col] = (pickPlace[col].split(',"'))
            for lin in range(len(pickPlace[col])):
                pickPlace[col][lin] = pickPlace[col][lin].replace('"', '')

            # Bottom Mirroring
            if pickPlace[col][-3] == "BottomLayer":
                pickPlace[col][2] = str("%.4f" % (x_size - float(pickPlace[col][2])))
                pickPlace[col][4] = str("%.4f" % (x_size - float(pickPlace[col][4])))
                pickPlace[col][6] = str("%.4f" % (x_size - float(pickPlace[col][6])))

            # Rotation Alteration
            pickPlace[col][-2] = str((int(pickPlace[col][-2]) - 90))

            # Removing N/M and TP's
            if pickPlace[col][-1] != "N/M" and pickPlace[col][-1] != "VALUE":
                buffer.append(pickPlace[col])

        outline = ""
        # Joining to a single vector
        for i in range(len(buffer)):
            buffer[i] = ",".join(buffer[i]) + "\n"

        # Ordering
        buffer.sort()

        # Adding Header
        buffer.insert(0, ",".join(['Designator', 'Footprint', 'Mid X', 'Mid Y', 'Ref X', 'Ref Y',
                                   'Pad X', 'Pad Y', 'Layer', 'Rotation', 'Comment']) + "\n")

        for i in range(len(buffer)):
            outline += buffer[i]

        # Exporting informations to a new .csv file
        outputFile = open(altiumOutputFile.name.replace(".csv", "_m.csv"), "w")
        outputFile.write(outline)
        outputFile.close()

        msg = QMessageBox()
        msg.setWindowTitle("File Configuration")
        msg.setText(f"Operation Successfully Completed")
        msg.exec_()
