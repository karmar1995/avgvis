from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore


class VisualObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getBoundingRect(self):
        top_left_x = self.x - int(self.width / 2)
        top_left_y = self.y - int(self.height / 2)
        return top_left_x, top_left_y, self.width, self.height

    def getShapePoints(self):
        points = list()
        shape_width = self.width/4
        shape_height = self.height/4
        origin_x = self.x
        origin_y = self.y - shape_height / 2
        points.append(QPoint(int(origin_x), int(origin_y)))
        points.append(QPoint(int(origin_x + shape_width/2), int(origin_y + shape_height)))
        points.append(QPoint(int(origin_x - shape_width/2), int(origin_y + shape_height)))
        return points


class VisualizationObjectWidget(QWidget):
    def __init__(self, parent, visualObject):
        super().__init__(parent=parent)
        self.__visualObject = visualObject

    def event(self, e: 'QEvent') -> bool:
        return super().event(e)

    def paintObject(self, painter):
        self.__drawObjectBackground(self.__visualObject, painter)
        self.__drawObjectBorder(self.__visualObject, painter)
        self.__drawObjectShape(self.__visualObject, painter)

    def __drawObjectBackground(self, visualObject, painter):
        brush = QBrush()
        brush.setColor(QColor(100, 100, 100, 50))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*visualObject.getBoundingRect())
        painter.fillRect(rect, brush)

    def __drawObjectBorder(self, visualObject, painter):
        brush = QBrush()
        brush.setColor(QColor(255, 0,0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*visualObject.getBoundingRect())
        pen = QPen()
        pen.setBrush(brush)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(rect)

    def __drawObjectShape(self, visualObject, painter):
        brush = QBrush()
        brush.setColor(QColor(0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        polygon = QPolygon(visualObject.getShapePoints())
        pen = QPen()
        pen.setBrush(brush)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawPolygon(polygon)


class MapWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.pixmap = QPixmap("/home/kmarszal/Documents/dev/avgvis/view/resources/map.png")
        self.visualObjects = list()

    def addObject(self, visualObject):
        self.visualObjects.append(VisualizationObjectWidget(self, visualObject))

    def paintEvent(self, e):
        painter = QPainter(self)
        brush = QBrush()
        brush.setTexture(self.pixmap)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)
        for visualObject in self.visualObjects:
            visualObject.paintObject(painter)
        painter.end()

    def sizeHint(self):
        return self.pixmap.size()


class MapPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.mapWidget = MapWidget(parent=parent)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.mapWidget)
        self.setLayout(self.mainLayout)
        self.newObjectX = 10
        self.newObjectY = 10

    def addColorObject(self):
        self.mapWidget.addObject(VisualObject(self.newObjectX, self.newObjectY, 200, 200))
        self.newObjectX += 400
        self.newObjectY += 300
        self.mapWidget.repaint()

class CentralWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.addObjectButton = QPushButton("Add visualization object")
        self.scrollArea = QScrollArea(parent=self)
        self.scrollAreaWidget = QWidget(parent=self.scrollArea)
        self.mapPane = MapPane(parent=self)
        layout = QVBoxLayout()
        layout.addWidget(self.mapPane)
        self.scrollAreaWidget.setLayout(layout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.addObjectButton)
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        self.addObjectButton.clicked.connect(self.__addObject)

    def __addObject(self):
        self.mapPane.addColorObject()

class Mainframe(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Visualization")
        self.setGeometry(100, 100, 1000, 1000)
        self.centralWidget = CentralWidget(parent=self)
        self.setCentralWidget(self.centralWidget)



