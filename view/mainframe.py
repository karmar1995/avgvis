from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
from view.properties_dialog import PropertiesDialog

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
        self.__hovered = False
        self.__popupMenu = QMenu()
        action = self.__popupMenu.addAction('Properties')
        action.triggered.connect(self.__onShowProperties)

    def __onShowProperties(self):
        props = {'a': 'b', 'c':'d', 'inna':'wartość'}
        dialog = PropertiesDialog(parent=self, properties=props)
        dialog.show()

    def __hoverLeaveEvent(self, e):
        self.__hovered = False

    def __hoverEnterEvent(self, e):
        self.__hovered = True

    def __showPopup(self, pos):
        self.__popupMenu.show()
        self.__popupMenu.move(pos)

    def __hidePopup(self):
        self.__popupMenu.hide()

    def __onRightMouseRelease(self, e):
        self.__showPopup(e.globalPosition().toPoint())

    def mouseReleaseEvent(self, e):
        self.__hidePopup()
        if e.button() == Qt.MouseButton.RightButton:
            self.__onRightMouseRelease(e)
        return super().mousePressEvent(e)

    def paintObject(self, painter):
        self.__drawObjectBackground(painter)
        self.__drawObjectBorder(painter)
        self.__drawObjectShape(painter)

    def event(self, e: QtCore.QEvent) -> bool:
        res = super().event(e)
        if e.type() == QEvent.Type.HoverEnter:
            self.__hoverEnterEvent(e)
        elif e.type() == QEvent.Type.HoverLeave:
            self.__hoverLeaveEvent(e)
        return res

    def rect(self) -> QtCore.QRect:
        return QtCore.QRect(*self.__visualObject.getBoundingRect())

    def __drawObjectBackground(self, painter):
        brush = QBrush()
        r, g, b, a = 0, 0, 0, 50
        if self.__hovered:
            a = 100
        brush.setColor(QColor(r, g, b, a))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*self.__visualObject.getBoundingRect())
        painter.fillRect(rect, brush)

    def __drawObjectBorder(self, painter):
        brush = QBrush()
        brush.setColor(QColor(255, 0,0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*self.__visualObject.getBoundingRect())
        pen = QPen()
        pen.setBrush(brush)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(rect)

    def __drawObjectShape(self, painter):
        brush = QBrush()
        brush.setColor(QColor(0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        polygon = QPolygon(self.__visualObject.getShapePoints())
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
        self.setMouseTracking(True)
        self.hoveredObject = None

    def addObject(self, visualObject):
        self.visualObjects.append(VisualizationObjectWidget(self, visualObject))

    def mouseReleaseEvent(self, e):
        pressedWidget = self.__getVisualObjectWidgetFromPoint(e.position())
        if pressedWidget:
            pressedWidget.mouseReleaseEvent(e)
        super().mouseReleaseEvent(e)
        
    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
        pos = e.position()

        oldHoveredWidget = self.hoveredObject

        hoveredWidget = self.__getVisualObjectWidgetFromPoint(pos)

        if self.hoveredObject != hoveredWidget:
            if self.hoveredObject:
                hoverLeavePos = pos
                hoverLeavePos -= self.hoveredObject.rect().topLeft().toPointF()
                hoverLeaveEvent = QHoverEvent(QEvent.Type.HoverLeave, hoverLeavePos, e.globalPosition(),
                                              e.globalPosition(), e.modifiers(), e.device())
                self.hoveredObject.event(hoverLeaveEvent)
            self.hoveredObject = hoveredWidget
            if self.hoveredObject:
                hoverEnterPos = pos
                hoverEnterPos -= hoveredWidget.rect().topLeft().toPointF()
                hoverEnterEvent = QHoverEvent(QEvent.Type.HoverEnter, hoverEnterPos, e.globalPosition(),
                                              e.globalPosition(), e.modifiers(), e.device())
                self.hoveredObject.event(hoverEnterEvent)

        if oldHoveredWidget != hoveredWidget:
            self.update()

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

    def __getVisualObjectWidgetFromPoint(self, pos):
        for visualObjectWidget in self.visualObjects:
            if visualObjectWidget.rect().contains(pos.toPoint()):
                return visualObjectWidget
        return None



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



