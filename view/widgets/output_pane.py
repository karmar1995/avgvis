from PyQt6.QtWidgets import *


class OutputWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.label = QLabel(parent=self)
        self.label.setText("Text")


class OutputDockWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.configurationWidget = OutputWidget(self)
        self.setWidget(self.configurationWidget)
        self.setWindowTitle("Output")