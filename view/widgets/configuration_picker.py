from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


CONFIG_EXTENSION = "json"


class ConfigurationPickerDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.__file = ""
        self.setWindowTitle("Select configuration file")
        self.lineEdit = QLineEdit()
        self.browseButton = QPushButton("Browse")
        self.newButton = QPushButton("New")
        self.applyButton = QPushButton("Apply")
        layout = QHBoxLayout()
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.browseButton)
        layout.addWidget(self.newButton)
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addStretch()
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.applyButton)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        self.browseButton.clicked.connect(self.__showBrowseDialog)
        self.newButton.clicked.connect(self.__showNewConfigDialog)
        self.applyButton.clicked.connect(self.__onApply)

    def getConfigurationPath(self):
        screenGeometry = QApplication.primaryScreen().geometry()
        windowGeometry = QRect()
        width = 600
        height = 400
        windowGeometry.setLeft(int(screenGeometry.width() / 2) - width)
        windowGeometry.setTop(int(screenGeometry.height() / 2) - height)
        windowGeometry.setWidth(width)
        windowGeometry.setHeight(height)
        self.setGeometry(windowGeometry)
        self.exec()
        return self.__file

    def __showBrowseDialog(self):
        self.__file = QFileDialog.getOpenFileName(parent=self,
                                                  caption="Open file",
                                                  directory="",
                                                  filter="Configuration files (*.{})".format(CONFIG_EXTENSION))[0]
        self.lineEdit.setText(self.__file)

    def __showNewConfigDialog(self):
        self.__file = QFileDialog.getSaveFileName(parent=self,
                                                  caption="Create file",
                                                  directory="",
                                                  filter="Configuration files (*.{})".format(CONFIG_EXTENSION))[0]
        self.lineEdit.setText(self.__file)

    def __onApply(self):
        self.close()