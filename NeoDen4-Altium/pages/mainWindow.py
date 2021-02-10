from PyQt5.QtWidgets import QSizePolicy, QWidget, QMainWindow, QPushButton, QGroupBox, QVBoxLayout, QGridLayout
from pages.fileName import FileNameWindow
from pages.fileConfig import FileConfigWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.buttonSetFileName = QPushButton('Set File Name')
        self.buttonSetFileName.setStyleSheet('QPushButton {background-color: #0000FF;font:bold}')
        self.buttonSetFileName.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.buttonSetFileName.clicked.connect(self.clickedSetFileName)

        self.buttonFileConfig = QPushButton('File Configuration')
        self.buttonFileConfig.setStyleSheet('QPushButton {background-color:#0000FF;font:bold}')
        self.buttonFileConfig.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.buttonFileConfig.clicked.connect(self.clickedFileConfig)

        self.loadWindow()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(self.buttonSetFileName, 0, 0)
        layout.addWidget(self.buttonFileConfig, 1, 0)

        self.horizontalGroupBox.setLayout(layout)

    def loadWindow(self):
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle("NeoDen4-Altium")

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)

        mainWidget = QWidget()
        mainWidget.setLayout(windowLayout)
        self.setCentralWidget(mainWidget)

    def clickedSetFileName(self):
        self.fileNameWind = FileNameWindow(self)
        self.fileNameWind.show()
        self.close()

    def clickedFileConfig(self):
        self.fileConfigWind = FileConfigWindow(self)
        self.fileConfigWind.show()
        self.close()
