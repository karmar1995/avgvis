from view.map_widget import *
from view.logic.map_widget_logic import *
from view.logic.user_view import *
from business_rules.composition_root import ViewInterfaces


class MapPane(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.mapWidget = MapWidget(parent=parent)
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.mapWidget)
        self.setLayout(self.mainLayout)


class CentralWidget(QWidget):
    def __init__(self, parent, startAppCallback):
        super().__init__(parent=parent)
        self.scrollArea = QScrollArea(parent=self)
        self.scrollAreaWidget = QWidget(parent=self.scrollArea)
        self.mapPane = MapPane(parent=self.scrollAreaWidget)
        self.startVisualizationButton = QPushButton(parent=self)
        self.startVisualizationButton.setText("Start visualization")
        layout = QVBoxLayout()
        layout.addWidget(self.startVisualizationButton)
        layout.addWidget(self.mapPane)
        self.scrollAreaWidget.setLayout(layout)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.scrollArea)
        self.setLayout(layout)
        self.startVisualizationButton.clicked.connect(startAppCallback)


class Mainframe(QMainWindow):
    def __init__(self, businessRules):
        super().__init__(parent=None)
        self.setWindowTitle("Visualization")
        self.setGeometry(100, 100, 1000, 1000)
        self.centralWidget = CentralWidget(parent=self, startAppCallback=self.__start)
        self.setCentralWidget(self.centralWidget)
        # composition root
        self.mapWidgetLogic = MapWidgetLogic(self.centralWidget.mapPane.mapWidget.mapAccess())
        self.modelViewAdapter = ModelViewToMapLogicAdapter(self.mapWidgetLogic)
        self.userViewAdapter = QtViewToAbstractUserView(self)
        self.businessRules = businessRules
        self.__initialize()

    def __initialize(self):
        modelView = self.modelViewAdapter
        userView = self.userViewAdapter
        viewInterfaces = ViewInterfaces(modelView=modelView, userView=userView)

        self.businessRules.setViewInterfaces(viewInterfaces)
        self.businessRules.initialize()

    def __start(self):
        self.businessRules.startApp()




