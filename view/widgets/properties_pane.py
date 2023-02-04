from PyQt6.QtWidgets import *


class PropertiesDockWidget(QDockWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.propertiesWidget = PropertiesWidget(parent = self, properties={})
        self.setWidget(self.propertiesWidget)
        self.setWindowTitle("Properties")


class PropertiesWidget(QWidget):
    
    def __init__(self, parent, properties):
        super().__init__(parent=parent)
        layout = QHBoxLayout()

        self.propertiesGrid = QTableWidget(self)
        self.propertiesGrid.setColumnCount(2)
        self.propertiesGrid.setHorizontalHeaderItem(0, QTableWidgetItem("Property"))
        self.propertiesGrid.setHorizontalHeaderItem(1, QTableWidgetItem("Value"))

        self.setProperties(properties)

        self.propertiesGrid.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.propertiesGrid)
        self.setLayout(layout)

    def setProperties(self, properties):
        self.propertiesGrid.setRowCount(len(properties))
        currentRow = 0
        for propertyName in properties:
            self.propertiesGrid.setItem(currentRow, 0, QTableWidgetItem(propertyName))
            self.propertiesGrid.setItem(currentRow, 1, QTableWidgetItem(properties[propertyName]))
            currentRow += 1
