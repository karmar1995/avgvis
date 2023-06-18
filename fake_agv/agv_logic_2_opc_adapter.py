class AgvLogic2OpcAdapter:
    def __init__(self, agvLogic, agvOpc):
        self.__agvLogic = agvLogic
        self.__agvOpc = agvOpc
        self.__agvLogic.addObserver(self)

    def onAgvStateChanged(self, agv):
        self.__agvOpc.setX(agv.x())
        self.__agvOpc.setY(agv.y())
