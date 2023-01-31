from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore


class PropertiesDialog(QDialog):
    
    def __init__(self, parent, properties):
        super().__init__(parent=parent)
        layout = QHBoxLayout()

        self.propertiesGrid = QTableWidget(self)
        self.propertiesGrid.setColumnCount(2)
        self.propertiesGrid.setRowCount(len(properties))
        self.propertiesGrid.setHorizontalHeaderItem(0, QTableWidgetItem("Property"))
        self.propertiesGrid.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))

        currentRow = 0
        for propertyName in properties:
            self.propertiesGrid.setItem(currentRow, 0, QTableWidgetItem(propertyName))
            self.propertiesGrid.setItem(currentRow, 1, QTableWidgetItem(properties[propertyName]))
            currentRow += 1

        self.propertiesGrid.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.propertiesGrid)
        self.setLayout(layout)
