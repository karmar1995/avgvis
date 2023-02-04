from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
from view.properties_dialog import PropertiesDialog
from view.logic.map_widget_logic import VisualizationWidgetLogic


class VisualizationObjectWidget(QWidget):
    def __init__(self, parent, widgetLogic : VisualizationWidgetLogic):
        super().__init__(parent=parent)
        self.__widgetLogic = widgetLogic
        self.__hovered = False
        self.__popupMenu = QMenu()
        action = self.__popupMenu.addAction('Properties')
        action.triggered.connect(self.__onShowProperties)

    def __onShowProperties(self):
        props = {'a': 'b', 'c': 'd', 'inna': 'wartość'}
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
        return QtCore.QRect(*self.__widgetLogic.getBoundingRect())

    def __drawObjectBackground(self, painter):
        brush = QBrush()
        r, g, b, a = 0, 0, 0, 50
        if self.__hovered:
            a = 200
        brush.setColor(QColor(r, g, b, a))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*self.__widgetLogic.getBoundingRect())
        painter.fillRect(rect, brush)

    def __drawObjectBorder(self, painter):
        brush = QBrush()
        brush.setColor(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        rect = QtCore.QRect(*self.__widgetLogic.getBoundingRect())
        pen = QPen()
        pen.setBrush(brush)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawRect(rect)

    def __drawObjectShape(self, painter):
        borderBrush = QBrush()
        borderBrush.setColor(QColor(0, 0, 0))
        borderBrush.setStyle(Qt.BrushStyle.SolidPattern)
        backgroundBrush = QBrush()
        backgroundBrush.setColor(QColor(50, 150, 50))
        backgroundBrush.setStyle(Qt.BrushStyle.SolidPattern)
        polygon = QPolygon(self.__pointsToQPoints(self.__widgetLogic.getShapePoints()))
        pen = QPen()
        pen.setBrush(borderBrush)
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawPolygon(polygon)
        painterPath = QPainterPath()
        painterPath.addPolygon(polygon.toPolygonF())
        painter.fillPath(painterPath, backgroundBrush)


    def __pointsToQPoints(self, points):
        qpoints = []
        for point in points:
            qpoints.append(QPoint(point.x, point.y))
        return qpoints


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


class GridWidget(QWidget):

    def __init__(self, parent, columnWidth, rowHeight):
        super().__init__(parent=parent)
        self.columnWidth = columnWidth
        self.rowHeight = rowHeight

    def setColumnWidth(self, columnWidth):
        self.columnWidth = columnWidth

    def setRowHeight(self, rowHeight):
        self.rowHeight = rowHeight

    def paintGrid(self, painter):
        self.__paintRows(painter)
        self.__paintColumns(painter)

    def __paintRows(self, painter):
        count = self.__calculateRowsCount()
        pointBegin = QPoint(0, 0)
        pointEnd = QPoint(self.parent().width(), 0)
        for i in range(0, count+1):
            self.__drawLine(pointBegin, pointEnd, painter)
            pointBegin.setY(pointBegin.y() + self.rowHeight)
            pointEnd.setY(pointEnd.y() + self.rowHeight)

    def __paintColumns(self, painter):
        count = self.__calculateColumnsCounts()
        pointBegin = QPoint(0, 0)
        pointEnd = QPoint(0, self.parent().height())
        for i in range(0, count+1):
            self.__drawLine(pointBegin, pointEnd, painter)
            pointBegin.setX(pointBegin.x() + self.columnWidth)
            pointEnd.setX(pointEnd.x() + self.columnWidth)

    def __drawLine(self, pointBegin, pointEnd, painter):
        brush = QBrush()
        brush.setColor(QColor(0, 0, 0))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        pen = QPen()
        pen.setBrush(brush)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(QLine(pointBegin, pointEnd))


    def __calculateRowsCount(self):
        return int(self.parent().height() / self.rowHeight)

    def __calculateColumnsCounts(self):
        return int(self.parent().width() / self.columnWidth)


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


