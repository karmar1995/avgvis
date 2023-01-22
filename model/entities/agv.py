from model.entities.visobject import *


class AgvObjectData:
    def __init__(self, visObjectData, battery):
        self.visObjectData = visObjectData
        self.battery = battery


class AgvObject(VisObject):
    def __init__(self, agvObjectData):
        super().__init__(agvObjectData.visObjectData)
        self.__battery = agvObjectData.battery

    def updateProperties(self, properties):
        self.__updateBattery(properties)

    def getBattery(self):
        return self.__battery

    def __updateBattery(self, properties):
        try:
            self.__battery = properties['battery']
        except KeyError:
            pass
