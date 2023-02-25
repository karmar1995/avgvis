from view.logic.mainframe_logic import MainframeLogic
from view.fakes.fake_ui.fake_alerts_widget import FakeAlertsWidget
from view.fakes.fake_ui.fake_map_widget import FakeMapWidget
from view.fakes.fake_ui.fake_output_widget import FakeOutputWidget
from view.fakes.fake_ui.fake_properties_widget import FakePropertiesWidget


class Mainframe:
    def __init__(self, businessRules):
        super().__init__(parent=None)
        self.mainframeLogic = MainframeLogic(businessRules)

        self.outputDockWidget = FakeOutputWidget(widgetLogic=self.mainframeLogic.outputLogic)
        self.alertsDockWidget = FakeAlertsWidget(widgetLogic=self.mainframeLogic.alerts)
        self.mapDockWidget = FakeMapWidget(widgetLogic=self.mainframeLogic.mapWidgetLogic)
        self.propertiesDockWidget = FakePropertiesWidget(widgetLogic=self.mainframeLogic.propertiesLogic)

        self.__initialize()

    def __initialize(self):
        self.mainframeLogic.initialize()

    def __start(self):
        self.mainframeLogic.start()

    def __stop(self):
        self.mainframeLogic.stop()


