from view.widgets.map_widget import *
from view.logic.map_widget_logic import *
from view.logic.user_view import *
from view.logic.selection import *
from view.logic.properties_logic import *
from view.logic.output_widget_logic import *
from business_rules.composition_root import ViewInterfaces
from view.widgets.map_dock_widget import MapDockWidget
from view.widgets.configuration_dock_widget import ConfigurationDockWidget
from view.widgets.properties_pane import PropertiesDockWidget
from view.widgets.alerts_pane import AlertsDockWidget
from view.widgets.output_pane import OutputDockWidget


class Mainframe(QMainWindow):
    def __init__(self, businessRules):
        super().__init__(parent=None)
        self.outputLogic = OutputWidgetLogic()

        self.setWindowTitle("Visualization")
        self.outputDockWidget = OutputDockWidget(parent=self, outputWidgetLogic=self.outputLogic)
        self.alertsDockWidget = AlertsDockWidget(parent=self)
        self.mapDockWidget = MapDockWidget(parent=self, startAppCallback=self.__start)
        self.propertiesDockWidget = PropertiesDockWidget(parent=self)
#        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea,  self.mapDockWidget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.propertiesDockWidget)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.alertsDockWidget)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.outputDockWidget)
        self.setCentralWidget(self.mapDockWidget)
        self.setTabPosition(Qt.DockWidgetArea.AllDockWidgetAreas, QTabWidget.TabPosition.North)

        # composition root
        self.selection = Selection()
        self.mapWidgetLogic = MapWidgetLogic(self.mapDockWidget.mapPane.mapWidget.mapAccess(), self.selection)
        self.propertiesLogic = PropertiesLogic(self.selection, self.propertiesDockWidget.propertiesWidget)
        self.modelViewAdapter = ModelViewToMapLogicAdapter(self.mapWidgetLogic)
        self.userViewAdapter = QtViewToAbstractUserView(self)
        self.businessRules = businessRules
        self.__initialize()

    def showMaximized(self) -> None:
        super().showMaximized()

    def __initialize(self):

        modelView = self.modelViewAdapter
        userView = self.userViewAdapter
        viewInterfaces = ViewInterfaces(modelView=modelView, userView=userView)

        self.businessRules.addErrorsListener(self.outputLogic)
        self.businessRules.setViewInterfaces(viewInterfaces)
        self.businessRules.initialize()

    def __start(self):
        self.businessRules.startApp()




