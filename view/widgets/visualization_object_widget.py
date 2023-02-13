from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import QtCore
from view.logic.map_widget_logic import VisualizationWidgetLogic


class VisualizationObjectWidget(QWidget):
    def __init__(self, parent, widgetLogic : VisualizationWidgetLogic):
        super().__init__(parent=parent)
        self.__widgetLogic = widgetLogic
        self.__hovered = False

    def __hoverLeaveEvent(self, e):
        self.__hovered = False

    def __hoverEnterEvent(self, e):
        self.__hovered = True

    def __onLeftMouseButtonReleased(self, e):
        self.__widgetLogic.updateSelection()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.__onLeftMouseButtonReleased(e)
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
        color = QColor(0, 0, 0, 50)
        if self.__widgetLogic.isSelected():
            color = QColor(50, 150, 50, 50)
        if self.__hovered:
            color = QColor(0, 0, 0, 150)
        brush.setColor(color)
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

