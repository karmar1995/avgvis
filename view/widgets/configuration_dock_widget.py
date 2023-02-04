from PyQt6.QtWidgets import *


class ConfigurationWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.label = QLabel(parent=self)
        self.label.setText("Text")


class ConfigurationDockWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.configurationWidget = ConfigurationWidget(self)
        self.setWidget(self.configurationWidget)
        self.setWindowTitle("Configuration")