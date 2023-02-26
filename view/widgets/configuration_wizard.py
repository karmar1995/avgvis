from PyQt6.QtWidgets import *


class FilePickerWidget(QWidget):
    def __init__(self, parent, label, buttonLabel):
        super().__init__(parent=parent)
        self.label = QLabel(label)
        self.lineEdit = QLineEdit()
        self.button = QPushButton(buttonLabel)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)


class LabeledSpinBox(QWidget):
    def __init__(self, parent, label):
        super().__init__(parent=parent)
        self.label = QLabel(label)
        self.spinbox = QDoubleSpinBox(parent=self)
        self.spinbox.setMinimum(-1000)
        self.spinbox.setMaximum(1000)
        self.spinbox.setDecimals(5)
        self.spinbox.setSingleStep(1)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        self.setLayout(layout)


class MapDataPage(QWizardPage):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.xSpinBox = LabeledSpinBox(self, "X: ")
        self.ySpinBox = LabeledSpinBox(self, "Y: ")
        self.widthSpinBox = LabeledSpinBox(self, "Width: ")
        self.heightSpinBox = LabeledSpinBox(self, "Height: ")
        self.filePicker = FilePickerWidget(self, "Map file: ", "Browse")
        layout = QVBoxLayout()
        layout.addWidget(self.filePicker)
        layout.addWidget(self.xSpinBox)
        layout.addWidget(self.ySpinBox)
        layout.addWidget(self.widthSpinBox)
        layout.addWidget(self.heightSpinBox)
        layout.addStretch()
        self.setLayout(layout)

    def initializePage(self):
        super().initializePage()


class AddObjectPage(QWizardPage):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.test = QPushButton("test2")
        layout = QHBoxLayout()
        layout.addWidget(self.test)
        self.setLayout(layout)

    def initializePage(self):
        super().initializePage()


class ConfigurationWizard(QWizard):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.__configurationPersistency = None
        self.addPage(MapDataPage(self))
        self.addPage(AddObjectPage(self))

    def driveConfiguration(self, persistency):
        self.__configurationPersistency = persistency
        self.exec()
