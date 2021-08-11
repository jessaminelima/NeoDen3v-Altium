from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QPushButton, QGroupBox, QVBoxLayout, QGridLayout,\
                            QAction, qApp, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from pages.fileConfig import FileConfigWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.pathfile = str()

    def initUI(self):
        toolbar = self.menuBar()
        fileMenu = toolbar.addMenu("&File")

        openAction = QAction("&Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip("Open")
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit application")
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.message = QLabel("Open a File")
        self.message.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.message.setAlignment(Qt.AlignCenter)

        self.buttonFileConfig = QPushButton("File Configuration")
        self.buttonFileConfig.setStyleSheet("QPushButton {background-color:#6495ED;font:bold}")
        self.buttonFileConfig.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.buttonFileConfig.clicked.connect(self.clickedFileConfig)

        self.loadWindow()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QGridLayout()

        layout.addWidget(self.message, 0, 0)
        layout.addWidget(self.buttonFileConfig, 1, 0)

        self.horizontalGroupBox.setLayout(layout)

    def loadWindow(self):
        self.setGeometry(700, 300, 300, 200)
        self.setWindowTitle("NeoDen3-Altium")

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)

        mainWidget = QWidget()
        mainWidget.setLayout(windowLayout)
        self.setCentralWidget(mainWidget)

    def clickedFileConfig(self):
        self.fileConfigWind = FileConfigWindow(self)
        self.fileConfigWind.show()
        self.close()

    def openFile(self):
        widget = QWidget()
        option = QFileDialog.Options()
        opened, _ = QFileDialog.getOpenFileName(widget, "Open File", "", "All Files(*)", options=option)
        self.pathfile = str(opened)
        self.message.setText(str(opened).split("/")[-1])
