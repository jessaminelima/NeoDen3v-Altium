from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QLineEdit, QLabel, QGroupBox, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt


class FileConfigWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.mainWindow = parent

        f = open(parent.pathfile, "r")
        self.file = (f.read())
        f.close()

        self.fileName = parent.pathfile

        self.text = QLabel("Put PCB X Size:")
        self.text.setAlignment(Qt.AlignCenter)

        self.xsize = QLineEdit("0")
        self.xsize.setAlignment(Qt.AlignCenter)

        self.unit = QLabel("mm")
        self.unit.setAlignment(Qt.AlignCenter)

        self.buttonCont = QPushButton("Continue")
        self.buttonCont.setStyleSheet("QPushButton {background-color:#6495ED;font:bold}")
        self.buttonCont.clicked.connect(self.clickedCont)

        self.buttonBack = QPushButton("Back")
        self.buttonBack.setStyleSheet("QPushButton {background-color:#999999;font:bold}")
        self.buttonBack.clicked.connect(self.clickedBack)

        self.loadWindow()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox2 = QGroupBox()
        layout = QGridLayout()
        layout2 = QGridLayout()

        layout.addWidget(self.text, 0, 0)
        layout.addWidget(self.xsize, 1, 0)
        layout.addWidget(self.unit, 1, 1)

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
        valuesToSave = float(self.xsize.text())
        self.buttonCont.setStyleSheet("QPushButton {background-color:#6495ED;font:bold}")
        self.Parameters(self.fileName, valuesToSave)

    def clickedBack(self):
        self.mainWindow.show()
        self.close()

    def Parameters(self, file, x_size):

        # Opening Altium .cvs file
        altiumOutputFile = open(file, "r", encoding="latin1")
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

            # Mirroring Bottom
            if pickPlace[lin][-4] == "BottomLayer":
                pickPlace[lin][2] = str("%.4f" % (x_size - float(pickPlace[lin][2])))
                pickPlace[lin][4] = str("%.4f" % (x_size - float(pickPlace[lin][4])))
                pickPlace[lin][6] = str("%.4f" % (x_size - float(pickPlace[lin][6])))

            # Rotation Alteration
            pickPlace[lin][-3] = str((int(pickPlace[lin][-3]) - 90))

            # Removing N/M and TP's
            if pickPlace[lin][-1] != "NM" and pickPlace[lin][-2] != "N/M" and pickPlace[lin][-2] != "VALUE":
                pickPlace[lin].pop(-1)  # Removing the last column created to inform NF components
                buffer.append(pickPlace[lin])

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
        msg.setText("Operation Successfully Completed")
        msg.exec_()
