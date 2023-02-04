from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
from view.logic.map_widget_logic import VisualizationWidgetLogic
from view.widgets.grid_widget import GridWidget
from view.widgets.visualization_object_widget import VisualizationObjectWidget


class MapAccess(QObject):
    def __init__(self, parent, mapWidget):
        super().__init__(parent=parent)
        self.mapWidget = mapWidget

    def showMap(self):
        self.mapWidget.showMapSignal.emit()

    def addObject(self, visualizationWidgetLogic):
        self.mapWidget.addObjectSignal.emit(visualizationWidgetLogic)

    def eraseObject(self, visualizationWidgetLogicId):
        pass

    def updateView(self):
        self.mapWidget.update()

    def size(self):
        return self.mapWidget.size()

    def updateGrid(self, columnWidth, rowHeight):
        self.mapWidget.updateGridSignal.emit(int(columnWidth), int(rowHeight))


class MapWidget(QWidget):
    showMapSignal = pyqtSignal(name='showMapSignal')
    addObjectSignal = pyqtSignal(VisualizationWidgetLogic, name="addObjectSignal")
    updateGridSignal = pyqtSignal(int, int, name="updateGridSignal")

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.pixmap = QPixmap("/home/kmarszal/Documents/dev/avgvis/view/resources/map.png")
        self.visualObjects = list()
        self.setMouseTracking(True)
        self.hoveredObject = None
        self.setFixedSize(self.pixmap.size())
        self.setVisible(False)
        self.__mapAccess = MapAccess(self, self)
        self.showMapSignal.connect(self.showMap)
        self.addObjectSignal.connect(self.addObject)
        self.updateGridSignal.connect(self.updateGrid)
        self.gridWidget = GridWidget(parent=self, columnWidth=100, rowHeight=100)

    def addObject(self, widgetLogic : VisualizationWidgetLogic):
        self.visualObjects.append(VisualizationObjectWidget(self, widgetLogic))

    def showMap(self):
        self.setVisible(True)

    def updateGrid(self, columnWidth, rowHeight):
        self.gridWidget.setColumnWidth(columnWidth)
        self.gridWidget.setRowHeight(rowHeight)

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
        rect = QtCore.QRect(0, 0, self.pixmap.width(), self.pixmap.height())
        painter.fillRect(rect, brush)
        for visualObject in self.visualObjects:
            visualObject.paintObject(painter)
        self.gridWidget.paintGrid(painter)
        painter.end()

    def __getVisualObjectWidgetFromPoint(self, pos):
        for visualObjectWidget in self.visualObjects:
            if visualObjectWidget.rect().contains(pos.toPoint()):
                return visualObjectWidget
        return None

    def mapAccess(self):
        return self.__mapAccess

    def sizeHint(self) -> QtCore.QSize:
        return self.pixmap.size()
