from view.widgets.map_widget import *
from view.logic.mainframe_logic import MainframeLogic
from view.widgets.map_dock_widget import MapDockWidget
from view.widgets.configuration_dock_widget import ConfigurationDockWidget
from view.widgets.properties_pane import PropertiesDockWidget
from view.widgets.alerts_pane import AlertsDockWidget
from view.widgets.output_pane import OutputDockWidget
from PyQt6.QtCore import QCoreApplication


class Mainframe(QMainWindow):
    def __init__(self, businessRules):
        super().__init__(parent=None)
        self.mainframeLogic = MainframeLogic(businessRules)

        self.setWindowTitle("Visualization")
        self.outputDockWidget = OutputDockWidget(parent=self, outputWidgetLogic=self.mainframeLogic.outputLogic)
        self.alertsDockWidget = AlertsDockWidget(parent=self, logic=self.mainframeLogic.alerts)
        self.mapDockWidget = MapDockWidget(parent=self, startAppCallback=self.__start, mapWidgetLogic=self.mainframeLogic.mapWidgetLogic)
        self.propertiesDockWidget = PropertiesDockWidget(parent=self, propertiesLogic=self.mainframeLogic.propertiesLogic)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.propertiesDockWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.alertsDockWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.outputDockWidget)
        self.setCentralWidget(self.mapDockWidget)
        self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)
        QCoreApplication.instance().aboutToQuit.connect(self.__stop)

        self.__initialize()

    def showMaximized(self) -> None:
        super().showMaximized()

    def __initialize(self):
        self.mainframeLogic.initialize()

    def __start(self):
        self.mainframeLogic.start()

    def __stop(self):
        self.mainframeLogic.stop()


