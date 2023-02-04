from PyQt6.QtWidgets import *
from view.widgets.map_pane import MapPane


class MapDockWidget(QDockWidget):
    def __init__(self, parent, startAppCallback):
        super().__init__(parent=parent)
        self.mapPane = MapPane(parent=self, startAppCallback=startAppCallback)
        self.setWidget(self.mapPane)
        self.setWindowTitle("Visualization")
