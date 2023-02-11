from PyQt6.QtWidgets import *


class AlertsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.label = QLabel(parent=self)
        self.label.setText("Text")


class AlertsDockWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setWidget(AlertsWidget(self))
        self.setWindowTitle("Alerts")