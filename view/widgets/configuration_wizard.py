from PyQt6.QtWidgets import *
from collections import namedtuple

ObjectData = namedtuple("ObjectData", "name sourceType connectionString width height xSignal ySignal headingSignal properties alerts updateInterval")


class LabeledLineEdit(QWidget):
    def __init__(self, parent, label):
        super().__init__(parent=parent)
        self.label = QLabel(label)
        self.lineEdit = QLineEdit()
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)


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
        self.button.clicked.connect(self.__showFileDialog)

    def __showFileDialog(self):
        file = QFileDialog.getOpenFileName(parent=self,
                                                  caption="Pick map file",
                                                  directory="",
                                                  filter="Images (*.png *.bmp *.jpg)")[0]
        self.lineEdit.setText(file)


class LabeledSpinBox(QWidget):
    def __init__(self, parent, label, min, max, decimals, step):
        super().__init__(parent=parent)
        self.label = QLabel(label)
        self.spinbox = QDoubleSpinBox(parent=self)
        self.spinbox.setMaximum(max)
        self.spinbox.setMinimum(min)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSingleStep(step)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
        self.setLayout(layout)


class MapDataPage(QWizardPage):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.xSpinBox = LabeledSpinBox(self, "X: ", -1000, 1000, 5, 1)
        self.ySpinBox = LabeledSpinBox(self, "Y: ", -1000, 1000, 5, 1)
        self.widthSpinBox = LabeledSpinBox(self, "Width: ", 0, 1000, 5, 1)
        self.heightSpinBox = LabeledSpinBox(self, "Height: ", 0, 1000, 5, 1)
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


class PickObjectTypeWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.pickObjectTypeLabel = QLabel("Object type: ")
        self.pickObjectTypeCombo = QComboBox(parent=self)
        self.pickObjectTypeCombo.addItem("OPC")
        self.pickObjectTypeCombo.addItem("FAKE_OPC")
        self.addObjectButton = QPushButton("Add object")
        layout = QHBoxLayout()
        layout.addWidget(self.pickObjectTypeLabel)
        layout.addWidget(self.pickObjectTypeCombo)
        layout.addWidget(self.addObjectButton)
        layout.addStretch()
        self.setLayout(layout)


class TwoColumnsGrid(QWidget):
    def __init__(self, parent, firstColumnName, secondColumnName, buttonLabel):
        super().__init__(parent=parent)
        self.grid = QTableWidget()
        self.grid.setColumnCount(2)
        labels = list()
        labels.append(firstColumnName)
        labels.append(secondColumnName)
        self.grid.setHorizontalHeaderLabels(labels)
        self.button = QPushButton(buttonLabel)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addStretch()
        layout = QVBoxLayout()
        layout.addWidget(self.grid)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.button.clicked.connect(self.__addRow)
        self.grid.horizontalHeader().setStretchLastSection(True)

    def __addRow(self):
        rows = self.grid.rowCount()
        self.grid.setRowCount(rows+1)

    def dumpGrid(self):
        items = list()
        for i in range(0, self.grid.rowCount()):
            item = self.grid.item(i, 0).text(), self.grid.item(i, 1).text()
            items.append(item)
        return items


class AddObjectDialog(QDialog):
    def __init__(self, parent, sourceType, listener):
        super().__init__(parent=parent)
        self.name = LabeledLineEdit(parent=self, label="Name: ")
        self.sourceType = sourceType
        self.connectionString = LabeledLineEdit(parent=self, label="Connection string: ")
        self.width = LabeledSpinBox(self, "Width: ", 0, 1000, 5, 1)
        self.height = LabeledSpinBox(self, "Height: ", 0, 1000, 5, 1)
        self.xSignal = LabeledLineEdit(parent=self, label="X coordinate signal: ")
        self.ySignal = LabeledLineEdit(parent=self, label="Y coordinate signal: ")
        self.headingSignal = LabeledLineEdit(parent=self, label="Heading signal: ")
        self.propertiesGrid = TwoColumnsGrid(parent=parent, firstColumnName="Property name", secondColumnName="Property signal", buttonLabel="Add property")
        self.alertsGrid = TwoColumnsGrid(parent=parent, firstColumnName="Alerts name", secondColumnName="Alerts signals directory", buttonLabel="Add alerts directory")
        self.submitButton = QPushButton("Submit")
        layout = QVBoxLayout()
        layout.addWidget(self.name)
        layout.addWidget(self.connectionString)
        layout.addWidget(self.width)
        layout.addWidget(self.height)
        layout.addWidget(self.xSignal)
        layout.addWidget(self.ySignal)
        layout.addWidget(self.headingSignal)
        layout.addWidget(self.propertiesGrid)
        layout.addWidget(self.alertsGrid)
        layout.addWidget(self.submitButton)
        self.setLayout(layout)
        self.__listener = listener
        self.submitButton.clicked.connect(self.__onSubmit)

    def __onSubmit(self):
        objectData = ObjectData(name=self.name.lineEdit.text(),
                                sourceType=self.sourceType,
                                connectionString=self.connectionString.lineEdit.text(),
                                width=self.width.spinbox.value(),
                                height=self.height.spinbox.value(),
                                xSignal=self.xSignal.lineEdit.text(),
                                ySignal=self.ySignal.lineEdit.text(),
                                headingSignal=self.headingSignal.lineEdit.text(),
                                properties=self.propertiesGrid.dumpGrid(),
                                alerts=self.alertsGrid.dumpGrid(),
                                updateInterval=0.1)
        self.__listener.onObjectAdded(objectData)
        self.close()


class ObjectsView(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.objectsTreeView = QTreeWidget(parent=self)
        self.objectsTreeView.setColumnCount(2)
        self.objectsTreeView.setHeaderLabels({"Option", "Value"})
        layout = QHBoxLayout()
        layout.addWidget(self.objectsTreeView)
        self.setLayout(layout)

    def addObject(self, objectData):
        objectRoot = self.__createItem(self.objectsTreeView, "Name", objectData.name)
        self.__createItem(objectRoot, "Source type", objectData.sourceType)
        self.__createItem(objectRoot, "Connection string", objectData.connectionString)
        self.__createItem(objectRoot, "Width", objectData.width)
        self.__createItem(objectRoot, "Height", objectData.height)
        self.__createItem(objectRoot, "X coordinate signal", objectData.xSignal)
        self.__createItem(objectRoot, "Y coordinate signal", objectData.ySignal)
        self.__createItem(objectRoot, "Heading signal", objectData.headingSignal)
        propertiesRoot = self.__createItem(objectRoot, "Properties", "")
        for propertyItem in objectData.properties:
            self.__createItem(propertiesRoot, propertyItem[0], propertyItem[1])
        alertsRoot = self.__createItem(objectRoot, "Alerts", "")
        for alertItem in objectData.alerts:
            self.__createItem(alertsRoot, alertItem[0], alertItem[1])
        self.__createItem(objectRoot, "Update interval", objectData.updateInterval).setHidden(True)

        self.objectsTreeView.insertTopLevelItem(self.objectsTreeView.topLevelItemCount(), objectRoot)

    def __createItem(self, parent, firstColumn, secondColumn):
        item = QTreeWidgetItem(parent)
        item.setText(0, firstColumn)
        item.setText(1, str(secondColumn))
        return item


class AddObjectsPage(QWizardPage):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.objects = list()
        self.objectsView = ObjectsView(parent=parent)
        self.pickObjectTypeWidget = PickObjectTypeWidget(parent=self)
        layout = QVBoxLayout()
        layout.addWidget(self.objectsView)
        layout.addWidget(self.pickObjectTypeWidget)
        self.setLayout(layout)
        self.pickObjectTypeWidget.addObjectButton.clicked.connect(self.__showAddObjectDialog)

    def onObjectAdded(self, objectData):
        self.objectsView.addObject(objectData)
        self.objects.append(objectData)

    def __showAddObjectDialog(self):
        dialog = AddObjectDialog(parent=self, sourceType=self.pickObjectTypeWidget.pickObjectTypeCombo.currentText(), listener=self)
        dialog.exec()

    def initializePage(self):
        super().initializePage()


class ConfigurationWizard(QWizard):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.__configurationPersistency = None
        self.mapDataPage = MapDataPage(self)
        self.addObjectsPage = AddObjectsPage(self)
        self.addPage(self.mapDataPage)
        self.addPage(self.addObjectsPage)
        self.__mapData = None

    def driveConfiguration(self, persistency):
        self.__configurationPersistency = persistency
        self.exec()

    def validateCurrentPage(self):
        if self.currentPage() == self.mapDataPage:
            return self.__onMapDataChanged()
        if self.currentPage() == self.addObjectsPage:
            return self.__onObjectsChanged()
        return super().validateCurrentPage()

    def __onMapDataChanged(self):
        mapUrl = self.mapDataPage.filePicker.lineEdit.text()
        x = self.mapDataPage.xSpinBox.spinbox.value()
        y = self.mapDataPage.ySpinBox.spinbox.value()
        width = self.mapDataPage.widthSpinBox.spinbox.value()
        height = self.mapDataPage.heightSpinBox.spinbox.value()
        if len(mapUrl) > 0 and width != 0 and height != 0:
            self.__mapData = (mapUrl, x, y, width, height)
            return True
        return False

    def __onObjectsChanged(self):
        self.__configurationPersistency.saveMapData(self.__mapData)
        self.__configurationPersistency.saveObjects(self.addObjectsPage.objects)
        self.__configurationPersistency.write()
        return True