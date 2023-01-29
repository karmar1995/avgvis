from PyQt6.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QImage, QPixmap, QImageReader


class MapPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout()
        self.pixmap = QPixmap("/home/kmarszal/Documents/dev/avgvis/view/resources/map.png")
        self.label = QLabel(parent=self)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)



class Mainframe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualization")
        self.layout = QHBoxLayout()
        self.setGeometry(100, 100, 1000, 1000)
        self.mapPane = MapPane(parent=self)
        self.layout.addWidget(self.mapPane)
